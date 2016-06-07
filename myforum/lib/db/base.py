PER_PAGE = 3


class BaseManager:
    def __init__(self, db_service):
        self.db = db_service

    def convert_row(self, row):
        pass

    def internal_convert(self, row, convert_func):
        if convert_func:
            return convert_func(row)
        else:
            return self.convert_row(row)

    def convert_rows(self, rows, convert_func):
        result = []
        for r in rows:
            result.append(self.internal_convert(r, convert_func))
        return result

    def internal_execute(self, query, params, fetch=2, convert_func=None):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        if fetch == 1:
            row = cursor.fetchone()
            if row == None:
                return None
            return self.internal_convert(row, convert_func)
        elif fetch == 2:
            rows = cursor.fetchall()
            if rows == None:
                return None
            return self.convert_rows(rows, convert_func)
        connection.commit()

    def execute(self, query, params=None):
        self.internal_execute(query, params, fetch=0)

    def select_all(self, query, params=None, convert_func=None):
        return self.internal_execute(query, params, fetch=2, convert_func=convert_func)

    def select_one(self, query, params=None, convert_func=None):
        return self.internal_execute(query, params, fetch=1, convert_func=convert_func)

    def paginate(self, query, query_count, page, u_id=0):
        posts_count = 0;
        if u_id:
            params = (u_id,)
            posts_count = self.count_helper(query_count, params)
            pages, limit, offset = self.pagination_hepler(page, posts_count)
            if offset < 0:
                return None, 0
            q_params = (u_id, limit, offset,)
            return self.select_all(query, q_params), pages
        else:
            posts_count = self.count_helper(query_count)
            pages, limit, offset = self.pagination_hepler(page, posts_count)
            if offset < 0:
                return None, 0
            q_params = (limit, offset,)
            return self.select_all(query, q_params), pages

    def pagination_hepler(self, page, posts_count):
        pages, sep = divmod(posts_count, PER_PAGE)
        if sep:
            pages += 1
        if page == pages and sep != 0:
            return pages, sep, 0
        else:
            offset = posts_count - PER_PAGE * page
            return pages, PER_PAGE, offset

    def count_helper(self, query, params=()):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        index = cursor.fetchone()
        return index[0]
