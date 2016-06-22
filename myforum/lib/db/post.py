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
        if len(row) > 6:
            p.username = row[6]
        return p

    def add_post(self, item):
        query = '''
        INSERT INTO posts(post, date_time, user_agent, ip, user_id)
        VALUES(%s, %s, %s, %s, %s) returning post_id
        '''
        params = (item.post, item.date_time, item.user_agent, item.ip, item.user_id)
        return self.select_scalar(query, params)

    def delete_post(self, id, user_id, admin_mod):
        query = '''
        DELETE FROM "posts" WHERE post_id = %s and user_id = %s or post_id = %s and 1=%s'''
        params = (id,user_id,id,admin_mod,)
        self.execute(query, params)

    def get_by_id(self, id):
        query = '''
        SELECT * FROM posts WHERE post_id = %s'''
        params = (id,)
        return self.select_one(query, params)

    def update_post(self, item, user_id, admin_mod):
        query = '''
        UPDATE posts SET post = %s, date_time = %s, user_agent = %s, ip = %s
        WHERE post_id = %s and user_id = %s or post_id = %s and 1=%s '''
        params = (item.post, item.date_time, item.user_agent, item.ip, item.post_id, user_id,
                  item.post_id, admin_mod,)
        self.execute(query, params)

    def get_all_posts(self, page):
        query_count = '''
        SELECT COUNT (*) FROM posts '''
        query = '''
            select p.post_id, p.post, p.date_time, p.user_agent, p.ip, p.user_id, u.username as u_name
            from posts p join users u on p.user_id = u.id ORDER by post_id
            limit %s offset %s'''
        count_posts = self.count_helper(query_count)
        pages, limit, offset = self.pagination_hepler(page, count_posts)
        params = (limit, offset,)
        return self.paginate(query, params, offset), pages

    def get_user_posts(self, page, user_id):
        query = '''
        SELECT * from posts where user_id = %s order by post_id limit %s offset %s'''
        query_count = '''
        SELECT COUNT (*) FROM posts where user_id = %s
        '''
        count_posts = self.count_helper(query_count, (user_id,))
        pages, limit, offset = self.pagination_hepler(page, count_posts)
        params = (user_id, limit, offset,)
        return self.paginate(query, params, offset), pages

    def get_posts_by_tag(self, tag_id, page):
        query_count = '''
        select count (*) from posts where post_id in (select post_id from post_tag where tag_id = %s)'''
        query = '''
        select p.post_id, p.post, p.date_time, p.user_agent, p.ip, p.user_id, u.username as u_name
        from posts p join users u on p.user_id = u.id where post_id in
        (select post_id from post_tag where tag_id=%s) limit %s offset %s'''
        count_posts = self.count_helper(query_count, (tag_id,))
        pages, limit, offset = self.pagination_hepler(page, count_posts)
        params = (tag_id, limit, offset,)
        return self.paginate(query, params, offset),pages
