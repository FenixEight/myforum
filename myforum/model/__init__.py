class Comment(object):
	def __init__(self):
		self.id = None
		self.user_name = None
		self.comment_text = None
		self.creation_date = None

class User(object):
	def __init__(self):
		self.id = None
		self.username = None
		self.password = None
		self.admin_mod = None

class Post(object):
	def __init__(self):
		self.post_id = None
		self.post = None
		self.date_time = None
		self.user_agent = None
		self.ip = None
		self.user_id = None

class Tag(object):
	def __init__(self):
		self.tag_id = None
		self.tag = None




