from datetime import datetime

from myforum.lib.db.base import BaseManager
from myforum.model import Comment


class CommentManager(BaseManager):
    def convert_row(self, row):
        c = Comment()
        c.id = row[0]
        c.post_id = row[1]
        c.parent_id = row[2]
        c.date = row[3]
        c.comment_text = row[4]
        c.is_deleted = row[5]
        c.user_id = row[6]
        c.username = row[7]
        c.has_photo = row[8]
        return c

    def add_comment(self, comment):
        query = '''
        INSERT INTO comments(post_id, parent_id, date_time, comment, is_deleted, user_id)
        VALUES(%s, %s, %s, %s, False, %s)'''
        params = (comment.post_id, comment.parent_id, comment.date, comment.comment_text, comment.user_id)
        self.execute(query, params)

    def delete_comment(self,c_id, user_id):
        query = '''
        UPDATE comments SET is_deleted = 'True' WHERE id = %s and user_id = %s'''
        params = (c_id, user_id,)
        self.execute(query, params)

    def get_flat_comments(self, post_id):
        query = '''
        SELECT c.id, c.post_id, c.parent_id, c.date_time, c.comment, c.is_deleted,
         c.user_id, u.username, u.has_photo FROM comments c
          join users u on c.user_id = u.id WHERE post_id = %s order by c.date_time
         '''
        params = (post_id,)
        return self.select_all(query, params)

    def get_comments_tree(self, post_id):
        query = '''
        SELECT c.id, c.post_id, c.parent_id, c.date_time, c.comment, c.is_deleted,
         c.user_id, u.username, u.has_photo  FROM comments c
          join users u on c.user_id = u.id WHERE post_id = %s'''
        params = (post_id,)
        comments = self.select_all(query, params)
        result = []
        if comments:
            self.make_tree(0, result, comments)
        return result

    def make_tree(self, parent_id, result_comments, all_comments):
        for c in all_comments:
            if c.parent_id == parent_id:
                result_comments.append(c)
        for c in result_comments:
            self.make_tree(c.id, c.children, all_comments)
