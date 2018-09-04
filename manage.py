from flask import  Flask
from  flask_script import Manager
from flask_session import Session

from app.models import db
from app.user_views import user_blueprint
import redis

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/aj4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Flask

app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')


#  配置session
# 指定redis作为缓存数据库
app.config['SESSION_TYPE'] = 'redis'
# 指定访问哪一个redis，ip和端口
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)


db.init_app(app)
# 加载app
sess = Session()
sess.init_app(app=app)

manage = Manager(app=app)

if __name__ == '__main__':
    manage.run()