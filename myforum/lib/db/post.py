from myforum.lib.db.base import BaseManager
from myforum.model import Post

per_page = 3


class PostManager(BaseManager):
    def convert_row(self, row):
        p = Post()
        p.post_id = row[0]
        p.post = row[1]
        p.date_time = row[2]
        p.user_agent = row[3]
        p.ip = row[4]
        p.user_id = row[5]
        if len(row) > 6:
            p.username = row[6]

        return p

    def add_post(self, item):
        query = '''
        INSERT INTO posts(post, date_time, user_agent, ip, user_id)
        VALUES(%s, %s, %s, %s, %s)
        '''
        params = (item.post, item.date_time, item.user_agent, item.ip, item.user_id)
        self.execute(query, params)

    def delete_post(self, id):
        query = '''
        DELETE FROM "posts" WHERE post_id = %s'''
        params = (id,)
        self.execute(query, params)

    def get_by_id(self, id):
        query = '''
        SELECT * FROM posts WHERE post_id = %s'''
        params = (id,)
        return self.select_one(query, params)

    def update_post(self, item):
        query = '''
        UPDATE posts SET post = %s, date_time = %s, user_agent = %s, ip = %s
        WHERE post_id = %s'''
        params = (item.post, item.date_time, item.user_agent, item.ip, item.post_id)
        self.execute(query, params)

    def get_posts(self, page=1, u_id=0):
        if u_id:
            # by user id
            query = '''
            SELECT * from posts where user_id = %s order by post_id limit %s offset %s
            '''
            query_count = '''
            SELECT COUNT (*) FROM posts where user_id = %s
            '''
            return self.paginate(query, query_count, page, u_id)

        else:
            # all posts
            query = '''
            select p.post_id, p.post, p.date_time, p.user_agent, p.ip, p.user_id, u.username as u_name
            from posts p join users u on p.user_id = u.id ORDER by post_id
            limit %s offset %s'''
            query_count = '''
            SELECT COUNT (*) FROM posts
            '''
            return self.paginate(query, query_count, page)


