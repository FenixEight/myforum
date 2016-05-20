from myforum.lib.db.base import BaseManager
from myforum.model import User

class UserManager(BaseManager):

    def convert_row(self, row):
        u = User()
        u.id = row[0]
        u.username = row[1]
        u.password = row[2]
        u.admin_mod = row[3]
        return u
    def get_username_by_name(self, name):
            query = '''
            SELECT id, username, password, admin_mod
            FROM "users" where username = %s'''
            params = (name,)
            return self.select_one(query, params)
    def add_username(self, name, password):
        query = '''
        INSERT INTO "users"(username, password, admin_mod)
        VALUES(%s, %s, %s)'''
        params = (name, password, 0)
        self.execute(query,params)
        