
import os

# 基础路径(项目所在路径)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# static
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
# static路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# media路径
MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
# 保存图片的路径
UPLOAD_DIR = os.path.join(MEDIA_DIR, 'upload')
# 数据库配置
MYSQL_DATABASES = {
    'DRIVER': 'mysql',
    'HD': 'pymysql',
    'ROOT': 'root',
    'PASSWORD': 123456,
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'NAME': 'aj4',
}

REDIS_DATABASES = {
    'HOST': '127.0.0.1',
    'PORT': 6379,

}