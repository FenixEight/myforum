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
        print query
        print params
        connection = self.db.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        if fetch == 1:
            row = cursor.fetchone()
            return self.internal_convert(row, convert_func)
        elif fetch == 2:
            rows = cursor.fetchall()
            return self.convert_rows(rows, convert_func)
        connection.commit()

    def execute(self, query, params=None):
        self.internal_execute(query, params, fetch=0)

    def select_all(self, query, params=None, convert_func=None):
        return self.internal_execute(query, params, fetch=2, convert_func=convert_func)

    def select_one(self, query, params=None, convert_func=None):
        return self.internal_execute(query, params, fetch=1, convert_func=convert_func)




