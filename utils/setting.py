
import os

# 基础路径(项目所在路径)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# static路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# media路径
MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
# 保存图片的路径
UPLOAD_DIR = os.path.join(MEDIA_DIR, 'upload')