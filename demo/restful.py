from weibo import *
from flask import Flask, request
from flask_cors import CORS
from train import *


app = Flask(__name__)
CORS(app, supports_credentials=True)


def return_data(arr):
    return {
        'count': len(arr),
        'code': 0,
        'data': arr,
    }


def get(k, v=None):
    return request.args.get(k, request.form.get(k, v))


cnt = 0


@app.route('/hello')
def hello():
    global cnt
    cnt += 1
    return 'hello_world!,cnt={}'.format(cnt)


@app.route('/userhome/<user_id>', methods=['GET', 'POST'])
def userhome(user_id):
    weibo = Weibo()
    return weibo.get_user_home(user_id)


@app.route('/search_user/<nickname>', methods=['GET', 'POST'])
def search_user(nickname):
    weibo = Weibo()
    return return_data(weibo.get_user_id(nickname))


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
    user_id, page = get('user_id'), get('page', 1)
    return Weibo().get_mblogs(user_id, page)


@app.route('/get_comments', methods=['GET', 'POST'])
def get_comments():
    cid, page = get('cid'), get('page', 1)
    return Weibo().get_comments_by_mid(cid, page)


runner = None


@app.route('/inference/<data>', methods=['GET', 'POST'])
def inference_data(data):
    global runner
    if runner is None:
        cfg = Config.fromfile('configs/config1.py')
        cfg.update(Config.from_list(['--inference', '1']))
        runner = BaseRunner(cfg)
    output = runner.inference(data)
    res = {
        'count': output.shape[0],
        'data': torch.max(output, dim=-1, keepdim=False)[-1].cpu().numpy().tolist(),
        'prob': output.cpu().numpy().tolist(),
    }
    return res


@app.route('/inference', methods=['GET', 'POST'])
def inference():
    return inference_data(get('data'))


def embedding(data):
    global runner
    if runner is None:
        cfg = Config.fromfile('configs/config1.py')
        cfg.update(Config.from_list(['--inference', '1']))
        runner = BaseRunner(cfg)
    return runner.test_embedding(data)


@app.route('/embedding/<data>', methods=['GET', 'POST'])
def test_embedding():
    return embedding(data)


@app.route('/embedding/', methods=['GET', 'POST'])
def test_embedding_():
    return embedding("None")

@app.route('/get_hot/', methods=['GET', 'POST'])
def get_hot():
    return Weibo().get_hot()

@app.route('/get_hot/', methods=['GET', 'POST'])


if __name__ == '__main__':
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
