from myforum.lib.db.base import BaseManager


class AdminManager(BaseManager):
    def mod_on(self):
        query = '''UPDATE params SET status = 'on' WHERE param = 'moderation' '''
        self.execute(query)

    def mod_off(self):
        query = '''UPDATE params SET status = 'off' WHERE param = 'moderation' '''
        self.execute(query)

    def mod_status(self):
        query = '''SELECT status FROM params  WHERE param = 'moderation' '''
        return self.select_scalar(query)

    def approve_post(self, id):
        params = (id,)
        query = '''UPDATE posts SET status = 'approved' WHERE post_id = %s '''
        self.execute(query, params)

    def cancel_post(self, id):
        params = (id,)
        query = '''UPDATE posts SET status = 'canceled' WHERE post_id = %s '''
        self.execute(query, params)

    def ban_user(self,id):
        query_for_posts = '''UPDATE posts SET status = 'banned' WHERE user_id = %s '''
        query_for_user = '''UPDATE users SET admin_mod = -1 WHERE id = %s'''
        params = (id,)
        self.execute(query_for_posts, params)
        self.execute(query_for_user,params)

    def unban_user(self,id):
        query_for_user = '''UPDATE users SET admin_mod = 0 WHERE id = %s'''
        params = (id,)
        self.execute(query_for_user,params)

    def add_to_blacklist(self, id, ban_id):
        query = '''INSERT into ban(username, username_banned) VALUES(%s, %s)'''
        params = (id, ban_id)

        self.execute(query,params)

    def remove_from_blacklist(self, id, ban_id):
        query = '''DELETE from ban where username = %s and username_banned = %s'''
        params = (id, ban_id)
        self.execute(query,params)

    def blacklist_status(self, id,ban_id):
        query = '''SELECT username_banned FROM ban where username = %s and username_banned = %s'''
        params = (id, ban_id)
        return self.select_scalar(query,params)