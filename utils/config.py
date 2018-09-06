from utils.function import get_redisdb_url, get_mysqldb_url


class Config():
    # 数据库
    SQLALCHEMY_DATABASE_URI = get_mysqldb_url()
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    # redis
    SESSION_TYPE = 'redis'
    # 指定访问哪一个redis，ip和端口
    SESSION_REDIS = get_redisdb_url()
