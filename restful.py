from weibo import *
from mysql import *
from flask import Flask, request
from flask_cors import CORS
from train import *
from transform.base_tokenizer import *
import json
import datetime


app = Flask(__name__)
CORS(app, resources=r'/*')


def return_data(arr):
    if isinstance(arr, dict):
        return arr
    return {
        'count': len(arr),
        'code': 0,
        'data': arr,
    }


def get(k, v=None):
    return request.args.get(k, request.form.get(k, v))


cnt = 0
save_mysql = 1


def add_users(users):
    if not save_mysql:
        return
    keys1 = ('id', 'screen_name', 'img', 'gender')
    keys2 = ('user_id', 'nickname', 'profile_image_url', 'gender')
    lst = []
    for user in users:
        now = {}
        for k1, k2 in zip(keys1, keys2):
            if k1 in user:
                now[k2] = user[k1]
        now['gender'] = {'m': '男', 'f': '女'}[now['gender']]
        lst.append(now)
    mysql.add_users(lst)


def to_datetime(s):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    return str(datetime.datetime.strptime(s, GMT_FORMAT))


def add_blogs(blogs):
    if not save_mysql:
        return
    # key1->key2
    keys1 = ('mid', 'user_id', 'text', 'show_time', 'tool', 'up', 'retweet', 'comment')
    keys2 = ('id', 'user_id', 'text', 'time', 'tool', 'up', 'retweet', 'comment')
    lst = []
    for blog in blogs:
        now = {}
        for k1, k2 in zip(keys1, keys2):
            if k1 in blog:
                now[k2] = blog[k1]
        now['time'] = to_datetime(now['time'])
        lst.append(now)
    cnt = mysql.add_blogs(lst)
    print(f'add {cnt} blogs')


def add_comments(comments):
    if not save_mysql:
        return
    # key1->key2
    keys1 = ('id', 'mid', 'user_id', 'nickname', 'text', 'show_time', 'up')
    keys2 = ('id', 'mid', 'user_id', 'nickname', 'text', 'time', 'up')
    lst = []
    for comment in comments:
        now = {}
        for k1, k2 in zip(keys1, keys2):
            if k1 in comment:
                now[k2] = comment[k1]
        now['time'] = to_datetime(now['time'])
        lst.append(now)
    mysql.add_comments(lst)


@app.route('/hello')
def hello():
    global cnt
    cnt += 1
    return 'hello_world!,cnt={}'.format(cnt)


@app.route('/userhome/<user_id>', methods=['GET', 'POST'])
def userhome(user_id):
    weibo = Weibo()
    return weibo.get_user_mhome(user_id)


@app.route('/search_user/<nickname>', methods=['GET', 'POST'])
def search_user(nickname):
    weibo = Weibo()
    return return_data(weibo.search_user(nickname))


@app.route('/search_realtime', methods=['GET', 'POST'])
def search_realtime():
    weibo = Weibo()
    keyword, page, inference, tokenize = (
        get('keyword'),
        get('page', 1),
        get('inference', 0),
        get('tokenize', 0),
    )
    data = weibo.search_realtime(keyword, page)
    if inference and 'data' in data:
        data['data'] = _inference_datas(data['data'])
    if tokenize and 'data' in data:
        data['data'] = _tokenize_data(data['data'])
    add_blogs(data['data'])
    return return_data(data)


@app.route('/search_topic', methods=['GET', 'POST'])
def search_topic():
    weibo = Weibo()
    keyword, page, inference = get('keyword'), get('page', 1), get('inference', 0)
    data = weibo.search_topic(keyword, page)
    if inference and 'data' in data:
        data['data'] = _inference_datas(data['data'])
    return return_data(data)


@app.route('/search_hot', methods=['GET', 'POST'])
def search_hot():
    weibo = Weibo()
    keyword, page = get('keyword'), get('page', 1)
    return return_data(weibo.search_hot(keyword, page))


@app.route('/get_fans', methods=['GET', 'POST'])
def get_fans():
    user_id, page = get('user_id'), get('page', 1)
    res = Weibo().get_fans_m(user_id, page)
    add_users(res['data'])
    return res


@app.route('/get_follows', methods=['GET', 'POST'])
def get_follows():
    user_id, page = get('user_id'), get('page', 1)
    res = Weibo().get_follows_m(user_id, page)
    add_users(res['data'])
    return res


@app.route('/get_weibo', methods=['GET', 'POST'])
def get_weibo():
    user_id, page = get('user_id'), get('page', 1)
    return return_data(Weibo().get_blogs(user_id, page))


@app.route('/get_comment', methods=['GET', 'POST'])
def get_comment():
    cid, page = get('cid'), get('page', 1)
    return return_data(Weibo().get_comments(cid, page))


@app.route('/search/<keyword>', methods=['GET', 'POST'])
def search(keyword):
    weibo = Weibo()
    return weibo.search(keyword)


@app.route('/get_blogs', methods=['GET', 'POST'])
def get_blogs():
    user_id, page, inference, tokenize = (
        get('user_id'),
        get('page', 1),
        get('inference', 0),
        get('tokenize', 0),
    )
    data = Weibo().get_mblogs(user_id, page)
    add_blogs(data['data'])
    if inference and 'data' in data:
        data['data'] = _inference_datas(data['data'])
    if tokenize and 'data' in data:
        data['data'] = _tokenize_data(data['data'])
    return data


@app.route('/get_comments', methods=['GET', 'POST'])
def get_comments():
    mid, page = get('mid'), get('page', 1)
    res = Weibo().get_comments_m(mid, page)
    add_comments(res['data'])
    return res


runner = None
tokenizer = None


@app.route('/inference/<data>', methods=['GET', 'POST'])
def inference_data(data):
    global runner
    if runner is None:
        cfg = Config.fromfile('configs/inference/cnn_50_inference_acc99.6.py')
        cfg.update(Config.from_list(['--inference', '1']))
        runner = BaseRunner(cfg)
    output = runner.inference(data)
    res = {
        'count': output.shape[0],
        'data': torch.max(output, dim=-1, keepdim=False)[-1].cpu().numpy().tolist(),
        'prob': output.cpu().numpy().tolist(),
    }
    return res


def _inference_datas(data):
    def temp_prob(prob):
        if prob[0] > 0.65:
            return 0
        if prob[1] > 0.65:
            return 1
        return 2

    global runner
    if runner is None:
        cfg = Config.fromfile('configs/inference/cnn_50_inference_acc99.6.py')
        cfg.update(Config.from_list(['--inference', '1']))
        runner = BaseRunner(cfg)
    output = runner.inference([x.get('text') for x in data])
    # res = torch.max(output, dim=-1, keepdim=False)[-1].cpu().numpy().tolist()
    prob = output.cpu().numpy().tolist()
    for i in range(len(data)):
        data[i]['prob'] = prob[i]
        data[i]['label'] = temp_prob(prob[i])  # res[i]
    return data


@app.route('/inference', methods=['GET', 'POST'])
def inference_datas():
    data, count = json.loads(get('data')), get('count', 0)
    return {'count': len(data), 'data': _inference_datas(data)}


def _tokenize_data(data, remove_topic=0):
    global tokenizer
    tokenizer = BaseTokenizer()

    def _remove_topic(text):
        if remove_topic==0:
            return text
        lst = text.split('#')
        text = ''
        for i in range(0, len(lst), 2):
            text += lst[i]
        return text

    output = tokenizer([_remove_topic(x.get('text')) for x in data])
    for i in range(len(data)):
        data[i]['tokenize_result'] = output[i]
    return data


def embedding(data):
    global runner
    if runner is None:
        cfg = Config.fromfile('configs/inference/cnn_50_inference_acc99.6.py')
        cfg.update(Config.from_list(['--inference', '1']))
        runner = BaseRunner(cfg)
    return str(runner.test_embedding(data))


@app.route('/embedding/<data>', methods=['GET', 'POST'])
def test_embedding(data):
    return embedding(data)


@app.route('/embedding', methods=['GET', 'POST'])
def test_embedding_():
    return embedding("None")


@app.route('/get_hot', methods=['GET', 'POST'])
def get_hot():
    return return_data(Weibo().get_hot())


@app.route('/get_hot_m', methods=['GET', 'POST'])
def get_hot_m():
    return return_data(Weibo().get_hot_m())


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5000)

    # build runner
    # cfg = Config.fromfile('configs/config1.py')
    # cfg.update(Config.from_list(['--inference', '1']))
    # runner = BaseRunner(cfg)
    # print(runner.test_embedding("None"))

    # output = runner.inference(["开心！","好难过啊"])
    # res={
    #     'count':output.shape[0],
    #     'data':torch.max(output, dim=-1, keepdim=False)[-1].cpu().numpy().tolist(),
    #     'prob':output.cpu().numpy().tolist(),
    # }
    # print(res)
