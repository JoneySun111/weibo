import requests
from urllib import request, parse
import json
from lxml import etree
import traceback
from datetime import datetime, timedelta
import urllib
import time
from bs4 import BeautifulSoup
from mysql import *


def to_list(list_iterator):
    try:
        return [x for x in list_iterator]
    except:
        print("list_iterator to list error", list_iterator)
        return []


# def filter_(lst,key,value):
#     res=list(filter(lambda x:x.attrs))


class Weibo:
    FANS_PER_PAGE = 10

    def __init__(self):
        self.cookie = {
            'Cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWB9G_m9pdXDuHZy6gBjkmr5NHD95Qfeo-0ehBN1hBRWs4DqcjzCJvV9PLKUgRt; SUB=_2A25M9qUDDeRhGeNM7lER9CnEzzSIHXVsGMtLrDV6PUJbktCOLU7BkW1NTgdeFHVltP2a9lG3XYCpKk2tNiEDIoSh; _T_WM=40266921044; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode=10000011&lfid=102803&uicode=20000174'
        }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWB9G_m9pdXDuHZy6gBjkmr5NHD95Qfeo-0ehBN1hBRWs4DqcjzCJvV9PLKUgRt; SUB=_2A25M9qUDDeRhGeNM7lER9CnEzzSIHXVsGMtLrDV6PUJbktCOLU7BkW1NTgdeFHVltP2a9lG3XYCpKk2tNiEDIoSh; _T_WM=40266921044; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode=10000011&lfid=102803&uicode=20000174',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
        }
        pass

    @classmethod
    def get_all(cls, selector):
        '''获取所有节点信息'''
        lst = selector.xpath('//*')
        res = {x.text: x.items() for x in lst}
        return res

    @staticmethod
    def get_publish_time(info):
        """获取微博发布时间"""
        try:
            publish_time = info
            if u'刚刚' in publish_time:
                publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            elif u'分钟' in publish_time:
                minute = publish_time[: publish_time.find(u'分钟')]
                minute = timedelta(minutes=int(minute))
                publish_time = (datetime.now() - minute).strftime('%Y-%m-%d %H:%M')
            elif u'今天' in publish_time:
                today = datetime.now().strftime('%Y-%m-%d')
                time = publish_time[3:]
                publish_time = today + ' ' + time
                if len(publish_time) > 16:
                    publish_time = publish_time[:16]
            elif u'月' in publish_time:
                year = datetime.now().strftime('%Y')
                month = publish_time[0:2]
                day = publish_time[3:5]
                time = publish_time[7:12]
                publish_time = year + '-' + month + '-' + day + ' ' + time
            else:
                publish_time = publish_time[:16]
            return publish_time
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    @staticmethod
    def get_publish_tool(info):
        """获取微博发布工具"""
        try:
            if len(info.split(u'来自')) > 1:
                publish_tool = info.split(u'来自')[1]
            else:
                publish_tool = u'无'
            return publish_tool.strip()
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def handle_html(self, url):
        """处理html"""
        try:
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            return selector
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def html_str(self, url, cookie=True):
        """处理html"""
        try:
            if cookie:
                html = requests.get(url, cookies=self.cookie).content.decode('utf-8')
            else:
                html = requests.get(url).content.decode('utf-8')
            return html
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    cnt = 0

    def get_soup(self, url, cookies=True):
        """获取html"""
        try:
            if cookies:
                # html = requests.get(url, cookies=self.cookie).content
                html = requests.get(url, headers=self.headers).content
                Weibo.cnt += 1
                time.sleep(0.2)
            else:
                html = requests.get(url).content
                Weibo.cnt += 0.1
            soup = BeautifulSoup(html, 'html.parser')  # 文档对象
            if Weibo.cnt > 6:
                time.sleep(3)
                Weibo.cnt = 0
            return soup
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def str_to_time(self, text):
        """将字符串转换成时间类型"""
        if ':' in text:
            result = datetime.strptime(text, '%Y-%m-%d %H:%M')
        else:
            result = datetime.strptime(text, '%Y-%m-%d')
        return result

    def get_user_info(self, user_id, use_cookie=0):
        '''获取用户信息'''
        try:
            url = 'https://weibo.cn/{}/info'.format(user_id)
            soup = self.get_soup(url)
            # print(soup.prettify())
            res = {}
            try:
                res['img'] = soup.select('img[alt="头像"]')[0].attrs['src']
            except:
                ...
            selector = self.handle_html(url)
            nickname = selector.xpath('//title/text()')[0]
            nickname = nickname[:-3]
            if nickname == u'登录 - 新' or nickname == u'新浪':
                sys.exit(u'cookie错误或已过期,请重新获取')
            res['nickname'] = nickname
            res['user_id'] = user_id
            basic_info = selector.xpath("//div[@class='c'][3]/text()")
            zh_list = [u'性别', u'地区', u'生日', u'简介', u'认证', u'达人']
            en_list = [
                'gender',
                'location',
                'birthday',
                'description',
                'verified_reason',
                'talent',
                'education',
                'work',
            ]
            for i in basic_info:
                if i.split(':', 1)[0] in zh_list:
                    res[en_list[zh_list.index(i.split(':', 1)[0])]] = i.split(':', 1)[1].replace(
                        '\u3000', ''
                    )
            if selector.xpath("//div[@class='tip'][2]/text()")[0] == u'学习经历':
                res['education'] = selector.xpath("//div[@class='c'][4]/text()")[0][1:].replace(
                    u'\xa0', u' '
                )
                if selector.xpath("//div[@class='tip'][3]/text()")[0] == u'工作经历':
                    res['work'] = selector.xpath("//div[@class='c'][5]/text()")[0][1:].replace(
                        u'\xa0', u' '
                    )
            elif selector.xpath("//div[@class='tip'][2]/text()")[0] == u'工作经历':
                res['work'] = selector.xpath("//div[@class='c'][4]/text()")[0][1:].replace(
                    u'\xa0', u' '
                )
            '''微博数、关注数、粉丝数'''
            # user_info = selector.xpath("//div[@class='tip2']/*/text()")
            # print(user_info)
            # weibo_num = int(user_info[0][3:-1])
            # following = int(user_info[1][3:-1])
            # followers = int(user_info[2][3:-1])
            # res['weibo_num'] = weibo_num
            # res['following'] = following
            # res['followers'] = followers
            return res
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()
            return {}

    def get_user_mhome(self, user_id):
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'.format(user_id)
        s = self.html_str(url)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']['userInfo']
        obj['blogs'] = obj['statuses_count']
        obj['follows'] = obj['follow_count']
        obj['fans'] = obj['followers_count']
        obj['user_id'] = obj['id']
        obj['nickname'] = obj['screen_name']
        obj['img'] = obj['profile_image_url']
        return obj

    def get_blogs(self, user_id, page=1):  # 需要cookie
        """获取微博信息"""
        try:
            url = 'https://weibo.cn/{}?page={}'.format(user_id, page)
            soup = self.get_soup(url)
            # print(soup.prettify())
            blogs = soup.select('div[class="c"]')
            arr = []
            for blog in blogs:
                text = blog.select('span[class="ctt"]')
                if len(text) == 0:
                    continue
                text = text[0].text
                try:
                    is_original = '转发了' not in blog.select('span[class="cmt"]')[0].text
                except:
                    is_original = True
                info = blog.select('span[class="ct"]')[0].text
                time = Weibo.get_publish_time(info)
                tool = Weibo.get_publish_tool(info)
                id = blog.select('a[class="cc"]')[-1].attrs['href'].split('/')[-1].split('?')[0]
                a_list = list(filter(lambda x: '[' in x, [x.text for x in blog.select('a')]))
                now = {}
                for s in a_list:
                    x = s.split('[')[0]
                    y = s.split('[')[1][:-1]
                    if '万' in y:
                        y = float(y[:-1]) * 10000
                    elif '亿' in y:
                        y = float(y[:-1]) * 10 ** 8
                    if x == '赞':
                        now['up'] = y
                    elif x == '转发':
                        now['retweet'] = y
                    elif x == '评论':
                        now['comment'] = y
                arr.append(
                    {
                        'text': text,
                        'time': time,
                        'tool': tool,
                        'is_original': is_original,
                        'id': id,
                        **now,
                    }
                )
            return arr
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_home(self):
        '''获取微博主页'''
        # page=1
        # id=5319509655
        # url='https://m.weibo.cn/api/container/getIndex?uid={}&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%9B%9B%E5%B7%9D%E6%97%A5%E6%8A%A5&type=uid&value={}&containerid=107603{}&page={}'.format(id,id,id,page)
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_2879338501&page=1'
        s = self.html_str(url)
        print(s)

    def get_user_id(self, nickname, page=1):
        # 用户名需要URL编码后
        url = "https://s.weibo.com/user/&nickname={}&page={}".format(parse.quote(nickname), page)
        # print(url)
        soup = self.get_soup(url)
        # print(soup.prettify())
        if soup:
            arr = []
            nicknames = [x.text for x in soup.select('div a[class="name"]')]
            # ids=[x.attrs['uid'] for x in soup.select('a[class="s-btn-c"]')]#已关注获取不到
            ids = [
                x.attrs['href'].split('/')[-1] for x in soup.select('a[class="wb_url"]')
            ]  # 可能不是数字
            # ids=[x.attrs['uid'] for x in soup.select('a[action-type="deFollow"]')]
            images = [x.attrs['src'] for x in soup.select('div[class="avator"] a img')]
            for i in range(len(nicknames)):
                arr.append(
                    {
                        'nickname': nicknames[i],
                        'user_id': ids[i],
                        'img': images[i],
                    }
                )
        return arr

    def get_user_home(self, user_id):
        # 获取用户微博数、粉丝数、关注数
        url = 'https://weibo.cn/{}'.format(user_id)
        soup = self.get_soup(url)
        # print(soup.prettify())
        p = soup.select('div[class="tip2"]')[0]
        lst = [x.text for x in p.contents]
        lst = list(filter(lambda x: x != '\xa0', lst))

        def get_number(s):
            assert '[' in s and ']' in s
            x = s.split('[')[0]
            y = s.split('[')[1][:-1]
            if '万' in y:
                y = float(y[:-1]) * 10000
            elif '亿' in y:
                y = float(y[:-1]) * 10 ** 8
            if x == '微博':
                x = 'blogs'
            elif x == '关注':
                x = 'follows'
            elif x == '粉丝':
                x = 'fans'
            elif x == '分组':
                x = 'group'
            return x, int(y)

        res = {'user_id': user_id}
        for s in lst:
            x, y = get_number(s)
            res[x] = y
        try:
            res['pages'] = int(soup.select('input[name="mp"],[type="hidden"]')[0].attrs['value'])
        except:
            res['pages'] = 1
        return res

    def get_fans(self, user_id, page=1):
        # 获取粉丝列表
        url = 'https://weibo.cn/{}/fans?page={}'.format(user_id, page)
        soup = self.get_soup(url)
        # print(soup.prettify())
        p = soup.select('table tr')
        lst = []
        for s in p:
            img = s.select('td a img')[0].attrs['src']
            user_id = s.select('td[valign="top"] a')[0].attrs['href'].split('/')[-1]
            nickname = s.select('td[valign="top"] a')[1].text
            lst.append(
                {
                    'user_id': user_id,
                    'nickname': nickname,
                    'img': img,
                }
            )
        # print(lst)
        return lst

    def get_follows(self, user_id, page=1):
        # 获取粉丝列表
        url = 'https://weibo.cn/{}/follow?page={}'.format(user_id, page)
        soup = self.get_soup(url)
        # print(soup.prettify())
        p = soup.select('table tr')
        lst = []
        for s in p:
            img = s.select('td a img')[0].attrs['src']
            user_id = s.select('td[valign="top"] a')[0].attrs['href'].split('/')[-1]
            nickname = s.select('td[valign="top"] a')[1].text
            lst.append(
                {
                    'user_id': user_id,
                    'nickname': nickname,
                    'img': img,
                }
            )
        return lst

    def get_comments(self, cid, page=1):
        url = 'https://weibo.cn/comment/{}?page={}'.format(cid, page)
        # print(url)
        soup = self.get_soup(url)
        # print(soup.prettify())
        try:
            s = soup.select('div[id="pagelist"] div')[0].text.split(' ')[-1]
            now_page = s.split('/')[0]
            total_page = s.split('/')[-1][:-1]
        except:
            now_page = total_page = 1
        res = {'now_page': int(now_page), 'total_page': int(total_page)}
        lst = soup.select('div[class="c"]')
        data = []
        for p in lst:
            if 'id' not in p.attrs:
                continue
            id = p.attrs['id']
            if len(id) <= 10 or 'C_' not in id:
                continue
            a_lst = p.select('a')
            user_id = a_lst[0].attrs['href'].split('/')[-1]
            nickname = a_lst[0].text
            text = p.select('span[class="ctt"]')[0].text
            # print('text ',text,end=' ->')
            if '回复@' == text[:3] and ':' in text.split('回复@')[1]:
                text = text.split('回复@')[1].split(':')[1]
            # print(text)
            up = p.select('span[class="cc"] a')[0].text[2:-1]
            info = p.select('span[class="ct"]')[0].text
            time = Weibo.get_publish_time(info)
            tool = Weibo.get_publish_tool(info)
            data.append(
                {
                    'id': id,
                    'cid': cid,
                    'user_id': user_id,
                    'nickname': nickname,
                    'text': text,
                    'time': time,
                    'tool': tool,
                    'up': up,
                }
            )
        res['data'] = data
        return res

    def get_follows_m(self, user_id, page=1):
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{}&page={}'.format(
            user_id, page
        )
        s = self.html_str(url)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']['cards'][-1]
        data = []
        for x in obj['card_group']:
            user = x['user']
            user['scheme'] = x['scheme']
            user['str'] = user.get('verified_reason', user.get('description', ''))
            data.append(user)
        return {'data': data, 'count': len(data), 'code': 0, 'page': page}

    def get_fans_m(self, user_id, page=1):
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{}&page={}'.format(
            user_id, page
        )
        s = self.html_str(url)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']['cards'][-1]
        data = []
        for x in obj['card_group']:
            user = x['user']
            user['scheme'] = x['scheme']
            user['str'] = user.get('verified_reason', user.get('description', ''))
            data.append(user)
        return {'data': data, 'count': len(data), 'code': 0, 'page': page}

    def get_hot(self):
        # 获取热搜
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=seat%3D1%26pos%3D0_0%26dgr%3D0%26mi_cid%3D100103%26cate%3D10103%26filter_type%3Drealtimehot%26c_type%3D30%26display_time%3D1638685500%26pre_seqid%3D1631149142&luicode=10000011&lfid=231583'
        soup = self.get_soup(url)
        s = soup.prettify()
        res = []
        for x in s.split('key:#')[1:]:
            title = x[: x.find('#|')].encode('latin-1').decode('unicode_escape')
            if title not in res:
                res.append(title)
        return res

    def search(self, key):
        url = (
            'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{}'.format(
                key
            )
        )
        s = self.html_str(url)
        obj_json = json.loads(s)
        assert obj_json.get('ok', 0) == 1
        obj = obj_json['data']
        del obj['scheme'], obj['showAppTips']
        data = []
        blogs = []

        def dfs(x):
            if isinstance(x, str) or x is None:
                return
            if 'mblog' in x:
                blogs.append(x['mblog'])
            if 'card_group' in x:
                dfs(x['card_group'])
            for y in x:
                dfs(y)

        dfs(obj['cards'])
        for blog in blogs:
            user = blog['user']
            data.append(
                {
                    'time': Weibo.get_publish_time(blog['created_at']),
                    'mid': blog['mid'],
                    'retweet': blog['reposts_count'],
                    'comment': blog['comments_count'],
                    'up': blog['attitudes_count'],
                    'user_id': user['id'],
                    'nickname': user['screen_name'],
                    'profile_image_url': user['profile_image_url'],
                    'text': BeautifulSoup(blog['text'], 'html.parser').text.replace(
                        '#{}#'.format(key), ''
                    ),
                }
            )
        # print(data)
        return {'data': data, 'count': len(data), 'code': 0}

    def get_mblogs(self, user_id, page=1):
        url = 'https://m.weibo.cn/api/container/getIndex?uid={}&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%9B%9B%E5%B7%9D%E6%97%A5%E6%8A%A5&type=uid&value={}&containerid=107603{}&page={}'.format(
            user_id, user_id, user_id, page
        )
        s = self.html_str(url)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']
        for blog in obj['cards']:
            if 'mblog' not in blog:
                continue
            mblog = blog['mblog']
            user = mblog['user']
            data.append(
                {
                    'user_id': user['id'],
                    'nickname': user['screen_name'],
                    'profile_image_url': user['profile_image_url'],
                    'mid': mblog['mid'],
                    'retweet': mblog['reposts_count'],
                    'comment': mblog['comments_count'],
                    'up': mblog['attitudes_count'],
                    'tool': mblog['source'],
                    'scheme': blog['scheme'],
                    'text': BeautifulSoup(mblog['text'], 'html.parser').text,
                    'time': Weibo.get_publish_time(mblog['created_at']),
                    'show_time': mblog['created_at'],
                }
            )
        return {
            'data': data,
            'count': len(data),
            'code': 0,
            'page': page,
            'total': obj['cardlistInfo']['total'],
        }

    def get_comments_by_mid(self, mid, page=1):
        url = 'https://m.weibo.cn/api/comments/show?id={}&page={}'.format(mid, page)
        # print(url)
        s = self.html_str(url)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']
        res = {}
        res['total_number'] = obj['total_number']
        res['max'] = obj['max']
        for comment in obj['data']:
            user = comment['user']
            text = BeautifulSoup(comment['text'], 'html.parser').text
            if '回复@' == text[:3] and ':' in text.split('回复@')[1]:
                text = text.split('回复@')[1].split(':')[1]
            data.append(
                {
                    'nickname': user['screen_name'],
                    'user_id': user['id'],
                    'img': user['profile_image_url'],
                    'id': user['id'],
                    'mid': mid,
                    'text': text,
                    'time': Weibo.get_publish_time(comment['created_at']),
                }
            )
        return {
            'total_number': obj['total_number'],
            'max': obj['max'],
            'count': len(data),
            'data': data,
            'page': page,
            'code': 0,
        }

    def get_comments_m(self, mid, page=1):
        url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0&page={}'.format(
            mid, mid, page
        )
        s = self.html_str(url)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']
        res = {}
        res['total_number'] = obj['total_number']
        res['max'] = obj['max']
        for comment in obj['data']:
            user = comment['user']
            text = BeautifulSoup(comment['text'], 'html.parser').text
            if '回复@' == text[:3] and ':' in text.split('回复@')[1]:
                text = text.split('回复@')[1].split(':')[1]
            data.append(
                {
                    'nickname': user['screen_name'],
                    'user_id': user['id'],
                    'img': user['profile_image_url'],
                    'id': user['id'],
                    'mid': mid,
                    'text': text,
                    'up': comment['like_count'],
                    'time': Weibo.get_publish_time(comment['created_at']),
                    'show_time': comment['created_at'],
                }
            )
        return {
            'total_number': obj['total_number'],
            'max': obj['max'],
            'count': len(data),
            'data': data,
            'page': page,
            'code': 0,
        }

    def search_user(self, nickname):
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D{}%26t%3D0&page_type=searchall'.format(
            nickname
        )
        s = self.html_str(url, False)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']['cards'][-1]
        data = []
        for x in obj['card_group']:
            user = x['user']
            user['scheme'] = x['scheme']
            user['str'] = user.get('verified_reason', user.get('description', ''))
            data.append(user)
        return {'data': data, 'count': len(data), 'code': 0}

    def search_realtime(self, keyword, page=1):
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{}%26t%3D0&page_type=searchall&page={}'.format(
            keyword, page
        )
        s = self.html_str(url, False)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']
        for blog in obj['cards']:
            if 'mblog' not in blog:
                continue
            mblog = blog['mblog']
            user = mblog['user']
            data.append(
                {
                    'user_id': user['id'],
                    'nickname': user['screen_name'],
                    'profile_image_url': user['profile_image_url'],
                    'mid': mblog['mid'],
                    'retweet': mblog['reposts_count'],
                    'comment': mblog['comments_count'],
                    'up': mblog['attitudes_count'],
                    'tool': mblog['source'],
                    'scheme': blog['scheme'],
                    'text': BeautifulSoup(mblog['text'], 'html.parser').text,
                    'time': Weibo.get_publish_time(mblog['created_at']),
                    'show_time': mblog['created_at'],
                }
            )
        return {
            'data': data,
            'count': len(data),
            'code': 0,
            'page': page,
            'total': obj['cardlistInfo']['total'],
        }

    def search_hot(self, keyword, page=1):
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D{}%26t%3D0&page_type=searchall&page={}'.format(
            keyword, page
        )
        s = self.html_str(url, False)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']
        for blog in obj['cards']:
            if 'mblog' not in blog:
                continue
            mblog = blog['mblog']
            user = mblog['user']
            data.append(
                {
                    'user_id': user['id'],
                    'nickname': user['screen_name'],
                    'profile_image_url': user['profile_image_url'],
                    'mid': mblog['mid'],
                    'retweet': mblog['reposts_count'],
                    'comment': mblog['comments_count'],
                    'up': mblog['attitudes_count'],
                    'tool': mblog['source'],
                    'scheme': blog['scheme'],
                    'text': BeautifulSoup(mblog['text'], 'html.parser').text,
                    'time': Weibo.get_publish_time(mblog['created_at']),
                    'show_time': mblog['created_at'],
                }
            )
        return {
            'data': data,
            'count': len(data),
            'code': 0,
            'page': page,
            'total': obj['cardlistInfo']['total'],
        }

    def search_topic(self, keyword, page=1):
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D38%26q%3D{}%26t%3D0&page_type=searchall&page={}'.format(
            keyword, page
        )
        s = self.html_str(url, False)
        obj_json = json.loads(s)
        data = []
        if obj_json.get('ok', 0) != 1:
            return {'code': 1, 'data': data, 'count': len(data)}
        obj = obj_json['data']
        data = []
        for card in obj['cards'][-1]['card_group']:
            data.append(
                {
                    'name': card['title_sub'],
                    'pic': card['pic'],
                    'desc1': card['desc1'],
                    'desc2': card.get('desc2', None),
                    'scheme': card['scheme'],
                }
            )
        return {
            'data': data,
            'count': len(data),
            'code': 0,
            'page': page,
            'total': obj['cardlistInfo']['total'],
        }


weibo = Weibo()
# print(weibo.search_topic('腾讯',1))
# print(weibo.search_hot('字节跳动', 1))
# print(weibo.search_realtime('字节跳动'))
# print(weibo.search_user('zkl小同学'))
print(weibo.get_fans_m(5319509655))
# print(weibo.get_background(5319509655))
# weibo.get_follows(5319509655)
# print(weibo.get_mblogs(5319509655,17))
# print(weibo.get_hot())
# mid = weibo.search("立陶宛求助欧盟制裁中国")['data'][0]['mid']
# print(weibo.get_comments_m(4711323370260659,2))
# print(weibo.get_comments(id))
# print(weibo.get_blogs(1887344341))
# # # # weibo.get_home()
# arr = weibo.get_user_id('zkl小同学')
# user_id = arr[0].get('user_id')
# print(user_id)
# weibo.get_fans(user_id)
# print(weibo.get_follow(user_id))
# print(weibo.get_user_home(user_id))
# id='Ii78Ikb9Z'
# print(weibo.get_comments(id))
# mysql.add_comments(weibo.get_comments(id)['data'])
# print(arr[0])
# print(weibo.get_user_info(user_id))
# user_id=arr[0].get('user_id')
# print(mysql.update_user(user_id,**weibo.get_user_info(user_id)))
# print(weibo.get_user_info(user_id))
# print(weibo.get_weibo(user_id))

# print(mysql.add_user(**arr[0]))
# print(mysql.add_users(arr))

# print(mysql.query_all_users())
