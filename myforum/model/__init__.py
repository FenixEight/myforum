class Comment(object):
    def __init__(self):
        self.id = None
        self.post_id = None
        self.parent_id = 0
        self.date = None
        self.comment_text = None
        self.is_deleted = None
        self.user_id = None
        self.children = []
        self.level = 0


class User(object):
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.admin_mod = None
        self.has_photo = None


class Post(object):
    def __init__(self):
        self.post_id = None
        self.post = None
        self.date_time = None
        self.user_agent = None
        self.ip = None
        self.user_id = None
        self.status = None


class Tag(object):
    def __init__(self):
        self.tag_id = None
        self.tag = None
