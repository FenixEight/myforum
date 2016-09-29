from myforum.lib.db.base import BaseManager
from myforum.model import User


class UserManager(BaseManager):
    def convert_row(self, row):
        u = User()
        u.id = row[0]
        u.username = row[1]
        u.password = row[2]
        u.admin_mod = row[3]
        u.has_photo = row[4]
        return u

    def get_username_by_name(self, name):
        query = '''
            SELECT id, username, password, admin_mod, has_photo
            FROM "users" where username = %s'''
        params = (name,)
        return self.select_one(query, params)

    def add_username(self, name, password):
        query = '''
        INSERT INTO "users"(username, password, admin_mod, has_photo)
        VALUES(%s, %s, %s, False)'''
        params = (name, password, 0)
        self.execute(query, params)

    def get_user_by_id(self, user_id):
        query = '''
        SELECT * FROM users where id = %s
        '''
        params = (user_id,)
        return self.select_one(query, params)

    def photo_add(self, id):
        query = '''UPDATE users set has_photo = True where id = %s '''
        params = (id,)
        self.execute(query, params)

    def photo_remove(self, id):
        query = '''UPDATE users set has_photo = False where id = %s '''
        params = (id,)
        self.execute(query, params)
