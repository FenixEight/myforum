def paginate_user_posts(self, id, page=1):
        query_user = '''
        SELECT * from posts where user_id = %s order by post_id limit %s offset %s
        '''
        query_count = '''
        SELECT COUNT (*) FROM posts where user_id = %s
        '''
        count_params = (id,)
        posts_count = self.count_helper(query_count, count_params)
        pages, b = divmod(posts_count, per_page)
        if b:
            pages += 1
        if page == pages and b != 0:
            params1 = (id, b, 0,)
            return self.select_all(query_user, params1), pages
        else:
            off = posts_count - per_page * page
            params2 = (id, per_page, off,)
            return self.select_all(query_user, params2), pages