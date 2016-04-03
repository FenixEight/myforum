from datetime import datetime

from myforum.lib.db.base import BaseManager
from myforum.model import Comment


class CommentManager(BaseManager):
    def convert_row(self, row):
        c = Comment()
        c.id = row[0]
        c.user_name = row[1]
        c.comment_text = row[2]
        c.creation_date = row[3]
        return c

    def add(self, item):
        query = '''
            INSERT INTO "comment"(user_name, comment_text, creation_date)
            VALUES(%s, %s, %s)'''
        params = (item.user_name, item.comment_text, datetime.now())
        self.execute(query, params)

    def update(self, item):
        query = '''
            UPDATE "comment"
            SET user_name = %s, comment_text = %s
            WHERE comment_id = %s'''
        params = (item.user_name, item.comment_text, item.id)
        self.execute(query, params)

    def delete(self, id):
        query = '''
            DELETE FROM "comment"
            WHERE comment_id = %s'''
        params = (item.id,)
        self.execute(query, params)

    def get_all(self):
        query = '''
            SELECT comment_id, user_name, comment_text, creation_date
            FROM "comment"
            ORDER BY creation_date'''
        return self.select_all(query)

    def get_by_id(self, id):
        query = '''
            SELECT comment_id, user_name, comment_text, creation_date
            FROM "comment"
            WHERE comment_id = %s
            ORDER BY creation_date'''
        params = (id,)
        return self.select_one(query, params)


