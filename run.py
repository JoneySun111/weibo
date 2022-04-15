from dataloader.dataset import OldDataset
from weibo import *
from mysql import *
from time import time

total = 0
now = 1
start = 1
t = time()
weibo = Weibo()


def init_log(_total, _now=1):
    global total, now, t, start
    total = _total
    start = now = _now
    t = time()


def log(s=''):
    global total, now, t, start
    t1 = time() - t
    t2 = t1 / (now - start + 1) * (total - now)
    t2 = int(t2)
    print('{} [{} / {}], eta={}h{}m{}s'.format(s, now, total, t2 // 3600, t2 // 60 % 60, t2 % 60))
    now += 1


def fill_user_info():
    user_lst = mysql.query_all_users()
    for i in range(len(user_lst)):
        print(i, '%', len(user_lst))
        x = user_lst[i]
        user_id = x[0]
        if not user_id.isdigit():
            continue
        if x[3]:
            continue
        info = weibo.get_user_info(user_id)
        if 'user_id' in info:
            mysql.update_user(**info)


def write_blogs(userid, max_pages=10, _write_comments=False):
    last = 0
    if not isinstance(userid, list):
        userid = [userid]
    init_log(len(userid), last)
    for user_id in userid[last:]:
        log('write_blogs')
        try:
            pages = min(max_pages, weibo.get_user_home(user_id)['pages'])
            print(user_id, pages)
            for i in range(1, pages + 1):
                blogs = weibo.get_mblogs(user_id, i)['data']
                mysql.add_blogs(blogs=blogs)
                if _write_comments:
                    write_comments(blogs, 6)
        except Exception as e:
            print('{} error: {}'.format(user_id, e))


def expand_user_by_fans(userid, max_pages=20):
    if not isinstance(userid, list):
        userid = [userid]
    for i in range(len(userid)):
        user_id = userid[i]
        pages = min(
            max_pages,
            (weibo.get_user_home(user_id)['fans'] + Weibo.FANS_PER_PAGE) // Weibo.FANS_PER_PAGE,
        )
        print(i, '%', len(userid), user_id, pages)
        for j in range(1, pages + 1):
            users = weibo.get_fans(user_id, j)
            mysql.add_users(users)
            print(users)


def expand_user_by_follow(userid, max_pages=20):
    if not isinstance(userid, list):
        userid = [userid]
    for i in range(len(userid)):
        user_id = userid[i]
        pages = min(
            max_pages,
            (weibo.get_user_home(user_id)['follows'] + Weibo.FANS_PER_PAGE) // Weibo.FANS_PER_PAGE,
        )
        print(i, '%', len(userid), user_id, pages)
        for j in range(1, pages + 1):
            users = weibo.get_follow(user_id, j)
            mysql.add_users(users)
            print(users)


def write_comments(blogs, max_pages=20):
    cnt = 0
    last = 0
    if not isinstance(blogs, list):
        blogs = [blogs]
    # init_log(len(blogs), last)
    for blog in blogs[last:]:
        # log('write_comments')
        for i in range(1, max_pages + 1):
            if 'mid' not in blog:
                continue
            res = weibo.get_comments_by_mid(blog['mid'], i)
            if res['count'] == 0:
                break
            data = res.get('data')
            cnt = cnt + mysql.add_comments(data)
    return cnt


def write_hot(max_page=20):

    keys = weibo.get_hot()
    init_log(len(keys))
    for key in keys[4:]:
        cnt = 0
        for page in range(1, max_page + 1):
            res = weibo.search_realtime(key, page)
            if res.get('page', 0) == 0:
                break
            blogs = res.get('data')
            cnt = cnt + mysql.add_blogs(blogs)
            blogs = list(filter(lambda x: x.get('comment', 0) > 0, blogs))
            cnt = cnt + write_comments(blogs)

        for page in range(1, max_page + 1):
            res = weibo.search_hot(key, page)
            if res.get('page', 0) == 0:
                break
            blogs = res.get('data')
            cnt = cnt + mysql.add_blogs(blogs)
            blogs = list(filter(lambda x: x.get('comment', 0) > 0, blogs))
            cnt = cnt + write_comments(blogs, 10)
        log(f'{key} {cnt} comments finish')


def write_comments_label():
    import dataloader
    from restful import _inference_datas
    import torch

    init_log(800 * 1000 / 2000)
    with open("dataset/mydataset.data", "w", encoding='utf-8') as f:
        for i in range(1000000):
            comments = mysql.query_comments(where=None, page=i, page_size=2000)
            if len(comments) == 0:
                break
            input = []
            for comment in comments:
                id, text, label = comment[0], comment[5], comment[-1]
                input.append(
                    {
                        'id': id,
                        'text': text,
                        'label': label,
                    }
                )
            data = _inference_datas(input)
            for x in data:
                if len(x['text']) == 0:
                    continue
                f.write("{},{},{}\n".format(x['id'], x['label'], x['text']))
            log()


def test_acc():
    import dataloader
    from restful import _inference_datas
    import torch

    dataset = OldDataset(['dataset/mydataset_label.data'])
    # dataset = OldDataset(['dataset/dataset3_test.data'])
    batch_size = 100
    dataloader = torch.utils.data.DataLoader(dataset=dataset, batch_size=batch_size, shuffle=False)
    acc = torch.zeros([1])
    total = torch.zeros([1])
    for data in dataloader:
        input = [{'text': x} for x in data[0]]
        pred = _inference_datas(input)
        labels = [x['label'] for x in pred]
        pred = torch.tensor(labels)
        # print(data[1])
        # print(pred)
        acc += data[1].eq(pred).sum()
        total += len(data[1])
        # break
    print(acc, total, acc / total)


def split_dataset():
    lines = []
    with open("dataset/mydataset.data", "r", encoding='utf-8') as f1:
        lines += f1.readlines()
    print(len(lines))
    id = [x.split(',')[0] for x in lines]
    lines = [x[x.find(',') + 1 :] for x in lines]
    label = [x.split(',')[0] for x in lines]
    text = [x[x.find(',') + 1 :] for x in lines]
    data = list(zip(text, label, id))
    random.shuffle(data)
    cnt = 0
    res = []
    mp = {}
    for x in data:
        mp.setdefault(x[1], 0)
        mp[x[1]] += 1
    mp = {
        '0': 105652,
        '1': (33 * 10000 - 105652) / 2,
        '2': 33 * 10000 - (33 * 10000 - 105652) / 2 - 105652,
    }
    for x in data:
        mp[x[1]] -= 1
        if mp[x[1]] < 0:
            continue
        res.append(x)
    print(len(res))
    random.shuffle(res)
    # print(res[:10])
    # print(len(res))

    with open("dataset/mydataset_train.data", "w", encoding='utf-8') as f1:
        for x in res[:300000]:
            f1.write("{},{},{}".format(x[2], x[1], x[0]))
    with open("dataset/mydataset_test.data", "w", encoding='utf-8') as f1:
        for x in res[300000:]:
            f1.write("{},{},{}".format(x[2], x[1], x[0]))


if __name__ == '__main__':
    # write_comments_label()
    # split_dataset()
    test_acc()
    # write_hot(4)
    # write_blogs([x[0] for x in mysql.query_all_users()], max_pages=5, _write_comments=True)
    # fill_user_info([x[0] for x in mysql.query_all_users()])
    # write_blogs([x[0] for x in mysql.query_all_users()],3)
    # expand_user_by_fans([x[0] for x in mysql.query_all_users()],2)
    # print(list(filter(lambda x:x[-1]>0,mysql.query_blogs(0,1000))))
    # lst = list(
    #     filter(lambda x: x[-1] > 0, mysql.query_blogs(where=' comment>0', page=1, page_size=40000))
    # )
    # # print(len(lst))
    # write_comments(lst, 3)

    # print([x[0] for x in mysql.query_all_users()])
    # weibo=Weibo()
    # user_id=[3818660693,5825929770,5140163125,'hznuhise',2159294697,5568308864,2133261771,2795615424,5835851597,2267763487,5668931862,5658510669]
    # expand_user_by_follow(user_id)
    # expand_user_by_fans(user_id)
    # print(user_id)
    # print(weibo.get_weibo(1194611782))
    # write_blogs(1194611782)

    # write_blogs()
    # weibo=Weibo()
    # arr=weibo.get_user_id('7304384465')
    # print(arr)
    # mysql=mysql()
    # # print(mysql.add_user(**arr[0]))
    # print(mysql.add_users(arr))
