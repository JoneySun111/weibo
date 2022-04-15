import pymysql


class mysql:

    db = pymysql.connect(
        host='120.27.194.164',
        port=3306,
        user='Weibo',
        passwd='000711',
        db='Weibo',
        charset='utf8mb4',
    )

    @staticmethod
    def get_where(**kwargs):
        where = ''
        for k, v in kwargs.items():
            if len(where):
                where += 'and '
            where += "`{}`='{}'".format(k, v)
        return where

    @classmethod
    def do_sql(cls, sql):
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def query_all_users(
        cls,
    ):
        sql = 'select* from user order by rand()'
        return cls.do_sql(sql)

    @classmethod
    def query_all_blogs(
        cls,
    ):
        sql = 'select* from blog'
        return cls.do_sql(sql)

    @classmethod
    def query_blogs(cls, where=None, page=0, page_size=-1):
        sql = 'select* from blog'
        if where:
            sql += ' where {}'.format(where)
        if page or page_size != -1:
            assert page_size > 0
            sql += ' limit {},{}'.format(page * page_size, page_size)
        return cls.do_sql(sql)

    @classmethod
    def query_comments(cls, where=None, page=0, page_size=-1):
        sql = 'select * from comment'
        if where:
            sql += ' where {}'.format(where)
        if page or page_size != -1:
            assert page_size > 0
            sql += ' limit {},{}'.format(page * page_size, page_size)
        return cls.do_sql(sql)

    @classmethod
    def query_user(cls, user_id, **kwargs):
        kwargs['user_id'] = user_id
        sql = 'select* from user where {}'.format(mysql.get_where(**kwargs))
        return cls.do_sql(sql)

    @classmethod
    def add_user(cls, user_id, **kwargs):
        kwargs['user_id'] = user_id
        cursor = cls.db.cursor()
        sql = 'insert into user {} values{}'.format(
            str(tuple(kwargs.keys())).replace("'", '`'), tuple(kwargs.values())
        )
        res = cursor.execute(sql)
        cls.db.commit()
        return res

    @classmethod
    def add_users(cls, users):
        cnt = 0
        for x in users:
            try:
                cnt += cls.add_user(**x)
            except Exception as e:
                print(e)
                ...
        return cnt

    @classmethod
    def update_user(cls, user_id, **kwargs):
        if len(kwargs) == 0:
            return 0
        cursor = cls.db.cursor()
        sql = 'update user set {} where `user_id`={}'.format(
            mysql.get_where(**kwargs).replace('and', ','), user_id
        )
        print(sql)
        res = cursor.execute(sql)
        cls.db.commit()
        return res

    @classmethod
    def add_blog(cls, text, **kwargs):
        # select COLUMN_NAME from information_schema.COLUMNS where table_name = 'blog' and table_schema = 'Weibo';
        kwargs.setdefault('id', kwargs.get('mid'))
        keys = ('id', 'text', 'user_id', 'tool', 'time', 'is_original', 'up', 'retweet', 'comment')
        kwargs['text'] = text
        kwargs = dict(filter(lambda x: x[0] in keys, kwargs.items()))
        cursor = cls.db.cursor()
        sql = 'insert into blog {} values{}'.format(
            str(tuple(kwargs.keys())).replace("'", '`'), tuple(kwargs.values())
        )
        # print(sql)
        res = cursor.execute(sql)
        cls.db.commit()
        return res

    # @classmethod
    # def add_blogs(cls, user_id, blogs):
    #     # print(len(blogs),blogs)
    #     cnt = 0
    #     for x in blogs:
    #         try:
    #             cnt += cls.add_blog(**x, user_id=user_id)
    #         except Exception as e:
    #             print(e)
    #             ...
    #     return cnt
    @classmethod
    def add_blogs(cls, blogs):
        # print(len(blogs),blogs)
        cnt = 0
        for x in blogs:
            try:
                cnt += cls.add_blog(**x)
            except Exception as e:
                print(e)
                ...
        return cnt

    @classmethod
    def add_comment(cls, id, text, **kwargs):
        keys = ('id', 'cid', 'mid', 'user_id', 'nickname', 'text', 'time', 'tool', 'up', 'label')
        kwargs['id'] = id
        kwargs['text'] = text
        kwargs = dict(filter(lambda x: x[0] in keys, kwargs.items()))
        cursor = cls.db.cursor()
        sql = 'insert into comment {} values{}'.format(
            str(tuple(kwargs.keys())).replace("'", '`'), tuple(kwargs.values())
        )
        # print(sql)
        res = cursor.execute(sql)
        cls.db.commit()
        return res

    @classmethod
    def add_comments(cls, comments):
        cnt = 0
        for x in comments:
            try:
                cnt += cls.add_comment(**x)
            except Exception as e:
                print(e)
                ...
        return cnt


# mysql=mysql()
# # print(mysql.do_sql('select * from user'))
# mysql.add_user()
# print(mysql.query_all_users())
# print(mysql.query_comments(None,0,10))
if __name__ == '__main__':
    with open("dataset/blogs.log", "w+") as f:
        for i in range(1000):
            comments = mysql.query_blogs(None, i, 10000)
            if len(comments) == 0:
                break
            comments = list(map(lambda x: x[0].strip(), comments))
            comments = list(filter(lambda x: len(x) > 1, comments))
            f.write('\n'.join(comments))
            print(i, 'finish')
