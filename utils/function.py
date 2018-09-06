import redis
from flask_session import Session

from app.models import db
from utils.setting import MYSQL_DATABASES, REDIS_DATABASES


def init_ext(app):
    # 加载数据库
    db.init_app(app)
    # 加载app
    sess = Session()
    sess.init_app(app=app)

def get_mysqldb_url():
    DRIVER = MYSQL_DATABASES ['DRIVER']
    HD = MYSQL_DATABASES ['HD']
    ROOT = MYSQL_DATABASES ['ROOT']
    PASSWORD = MYSQL_DATABASES ['PASSWORD']
    HOST = MYSQL_DATABASES ['HOST']
    PORT = MYSQL_DATABASES ['PORT']
    NAME = MYSQL_DATABASES ['NAME']
    return '{}+{}://{}:{}@{}:{}/{}'.format(DRIVER, HD, ROOT, PASSWORD, HOST,PORT,NAME)


def get_redisdb_url():
    HOST = REDIS_DATABASES['HOST']
    PORT = REDIS_DATABASES['PORT']
    return redis.Redis(host=HOST, port=PORT)