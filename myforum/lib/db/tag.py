from myforum.lib.db.base import BaseManager
from myforum.model import Tag


class TagManager(BaseManager):
    def convert_row(self, row):
        t = Tag()
        t.tag_id = row[0]
        t.tag = row[1]
        return t

    def search_tag(self, tag):
        query = '''
        select * from tags where tag = %s'''
        params = (tag,)
        return self.select_one(query, params)

    def add(self, tag, post_id):
        t = self.search_tag(tag)
        if not t:
            tag_id = self.add_tag(tag)
            self.set_link(tag_id, post_id)
        else:
            self.set_link(t.tag_id, post_id)

    def add_tag(self, tag):
        query = '''
        insert into tags (tag) values(%s) returning tag_id'''
        params = (tag,)
        return self.select_scalar(query, params)

    def set_link(self, tag_id, post_id):
        query = '''
        insert into post_tag (post_id, tag_id) values(%s, %s)
        '''
        params = (post_id, tag_id,)
        self.execute(query, params)

    def update(self, post_id, old_tag_id, new_tag):
        self.delete_link(post_id, old_tag_id)
        self.add_tag(new_tag, post_id)

    def delete_link(self, post_id, tag_id):
        query = '''
        delete from post_tag where post_id = %s and tag_id = %s'''
        params = (post_id, tag_id,)
        self.execute(query, params)

    def get_tags_by_post_id(self, post_id):
        query = '''
        select * from tags where tag_id in (select tag_id from post_tag where post_id = %s)'''
        params = (post_id,)
        return self.select_all(query, params)

    def delete_links(self, post_id):
        query = '''
        delete from post_tag where post_id = %s'''
        params = (post_id,)
        self.execute(query, params)
