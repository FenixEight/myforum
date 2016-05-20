from myforum.lib.db.base import BaseManager
from myforum.model import Post

class PostManager(BaseManager):

    def convert_row(self, row):
        p = Post()
        p.post_id = row[0]
        p.post = row[1]
        p.date_time = row[2]
        p.user_agent = row[3]
        p.ip = row[4]
        p.user_id = row[5]
        return p
    def add_post(self, item):
        query = '''
        INSERT INTO posts(post, date_time, user_agent, ip, user_id)
        VALUES(%s, %s, %s, %s, %s)
        '''
        params = (item.post, item.date_time, item.user_agent, item.ip, item.user.id)
        self.execute(query, params)

    def delete_post(self,id):
        query = '''
        DELETE FROM "posts" WHERE post_id = %s'''
        params = (id,)
        self.execute(query,params)

    def get_by_id(self, id):
        query = '''
        SELECT FROM posts WHERE post_id = %s'''
        params = (id,)
        return self.select_one(query,params)

    def all_user_posts(self, id):
        query = '''
        SELECT (id, post, date_time, user_agent, ip, user_id) FROM posts
        WHERE user_id = %s
        '''
        params = (id,)
        return self.select_all(query,params)

    def update_post(self, item):
        query = '''
        UPDATE "posts" SET post = %s, date_time = %s, user_agent = %s, ip = %s
        WHERE post_id = %s'''
        params = (item.post, item.date_time, item.user_agent, item.ip, item.post_id)
        self.execute(query, params)

