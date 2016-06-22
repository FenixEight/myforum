import psycopg2
import psycopg2.extensions

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
from psycopg2.pool import ThreadedConnectionPool

from myforum.lib.db.comment import CommentManager
from myforum.lib.db.user import UserManager
from myforum.lib.db.post import PostManager
from myforum.lib.db.tag import TagManager


class DataService:
	def __init__(self, connection_string):
		self.connection_string = connection_string
		self.comment = CommentManager(self)
		self.user = UserManager(self)
		self.post = PostManager(self)
		self.tag = TagManager(self)

	def get_connection(self):
		return psycopg2.connect(self.connection_string)
