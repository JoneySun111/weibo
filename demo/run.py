from weibo import *
from mysql import *
from time import time

total = 0
now = 1
start = 1
t = time()


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
    weibo = Weibo()
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


def write_blogs(userid, max_pages=10):
    last = 155
    weibo = Weibo()
    if not isinstance(userid, list):
        userid = [userid]
    init_log(len(userid), last)
    for user_id in userid[last:]:
        log('write_blogs')
        try:
            pages = min(max_pages, weibo.get_user_home(user_id)['pages'])
            print(user_id, pages)
            for i in range(1, pages + 1):
                blogs = weibo.get_blogs(user_id, i)
                mysql.add_blogs(user_id=user_id, blogs=blogs)
        except:
            print('{} error'.format(user_id))


def expand_user_by_fans(userid, max_pages=20):
    weibo = Weibo()
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
    weibo = Weibo()
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


def write_comments(cid, max_pages=20):
    weibo = Weibo()
    if not isinstance(cid, list):
        cid = [cid]
    for now_id in cid:
        for i in range(1, max_pages + 1):
            res = weibo.get_comments(now_id, i)
            total_page = res['total_page']
            data = res.get('data')
            mysql.add_comments(data)
            if i >= total_page:
                break


def write_all_comments(blogs, max_pages=20):
    last = 0
    weibo = Weibo()
    if not isinstance(blogs, list):
        blogs = [blogs]
    init_log(len(blogs), last)
    for blog in blogs[last:]:
        log('write_all_comments')
        write_comments(blog[0], max_pages)


if __name__ == '__main__':
    # fill_user_info()
    # write_blogs([x[0] for x in mysql.query_all_users()],3)
    # expand_user_by_fans([x[0] for x in mysql.query_all_users()],2)
    # print(list(filter(lambda x:x[-1]>0,mysql.query_blogs(0,1000))))
    lst = list(
        filter(lambda x: x[-1] > 0, mysql.query_blogs(where=' comment>0', page=1, page_size=40000))
    )
    # print(len(lst))
    write_all_comments(lst, 3)

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
