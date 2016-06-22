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

    def internal_execute(self, query, params, fetch=None, convert_func=None):
        connection = self.db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            if fetch == 'one':
                row = cursor.fetchone()
                if row:
                    return self.internal_convert(row, convert_func)
            elif fetch == 'all':
                rows = cursor.fetchall()
                if rows:
                    return self.convert_rows(rows, convert_func)
            elif fetch == 'scalar':
                row = cursor.fetchone()
                print(row)
                if row:
                    return row[0]
        finally:
            connection.commit()

    def execute(self, query, params=None):
        self.internal_execute(query, params)

    def select_scalar(self, query, params=None):
        return self.internal_execute(query, params, fetch='scalar')

    def select_all(self, query, params=None, convert_func=None):
        return self.internal_execute(query, params, fetch='all', convert_func=convert_func)

    def select_one(self, query, params=None, convert_func=None):
        return self.internal_execute(query, params, fetch='one', convert_func=convert_func)

    def paginate(self, query, params, offset):
        if offset < 0:
            return None
        else:
            return self.select_all(query, params)

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
