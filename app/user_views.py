import random
import re
import os

from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for

from app.models import db, User
from utils import status_code
from utils.setting import UPLOAD_DIR



# 定义蓝图
user_blueprint = Blueprint('user', __name__)

#定义一个修饰器用来审查cookie中的session_id
def log(func):
    def wrapper(*args, **kw):
        user = session.get('user_id')
        if user is None:
            return redirect(url_for('user.login'))
        return func(*args, **kw)
    return wrapper


# 创建模型数据库表
@user_blueprint.route('create_all/')
def create_all():
    db.create_all()
    return '创建成功'


# 进入注册页面
@user_blueprint.route('register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')


# 4位数随机验证码生成
@user_blueprint.route('img_code/', methods=['GET'])
def img_code():
    s = 'qwertyuiopasdfghjklzxcvbnm7899456123'
    data = ''
    for i in range(4):
        data += random.choice(s)
    session['code'] = data
    return jsonify({'code':200, 'msg': '请求成功', 'data': data})


# 实现注册
@user_blueprint.route('registerqpost/', methods=['POST'])
def my_register():
    # 获得页面提交数据
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 校验是否填写完整
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify(status_code.USER_REGISTER_PARAMS_NOT_EXISTS)
    # 校验手机号
    if not re.match(r'^1[345678]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_PHONE_IS_NOT_VALID)
    # 校验图片验证码
    if session.get('code') != imagecode:
        return jsonify(status_code.USER_REGISTER_CODE_IS_NOT_VALID)
    # 校验密码是否一致
    if passwd2 != passwd:
        return jsonify(status_code.USER_REGISTER_PASSWORD_NOT_EQUAL)
    # 校验电话是否注册
    user = User.query.filter(User.phone==mobile).all()
    if user:
        return jsonify(status_code.USER_REGISTER_PHONE_IS_EXISTS)
    # 保存信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify(status_code.SUCCESS)


# 进入登录页面
@user_blueprint.route('login/',methods=['GET'])
def login():
    return render_template('login.html')


# 验证登录信息是否正确
@user_blueprint.route('my_login/', methods=['GET'])
def my_login():
    mobiler = request.args.get('mobile')
    password = request.args.get('password')
    # 校验是否填写完整
    if not all([mobiler, password]):
        return jsonify(status_code.USER_LOGIN_PARAMS_NOT_EXISTS)
    # 校验手机号
    if not re.match(r'1[345678]\d{9}', mobiler):
        return jsonify(status_code.USER_LOGIN_PHONE_IS_NOT_VALID)
    # 校验手机号是否存在
    user = User.query.filter(User.phone == mobiler).first()
    # 校验用户是否存在
    if not user:
        return jsonify(status_code.USER_LOGIN_IS_NOT_EXISTS)
    # 校验密码是否正确
    if not user.check_pwd(password):
        return jsonify(status_code.USER_LOGIN_PASSWORD_IS_NOT_VALID)
    #将用户写进session中
    session['user_id'] = user.id
    return jsonify(status_code.SUCCESS)


# 进入个人主页（@log是判断是否登录的装饰器）
@user_blueprint.route('my/', methods=['GET'])
@log
def my():
    return render_template('my.html')

#  进入个人主页面后自动回调的个人信息
@user_blueprint.route('my_info/', methods=['GET'])
def my_info():
    # 获取在login页面登录时，写在session中的user_ia
    user_id = session['user_id']
    # 通过id拿到数据库用户对象
    user = User.query.get(user_id)
    # 调用user的类方法拿到用户是基本信息(返回给ajax的是json文件，而不是一个对象)
    user_info = user.to_basic_dict()
    # 创建一个code用判断
    code = 200
    return jsonify(user_info=user_info, code=code)


# 退出登录，清空session中的值，反向解析login页面
@user_blueprint.route('logout/', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('user.login'))


# 头像上传修改要页面
@user_blueprint.route('profile/', methods=['GET'])
def profile():
    return render_template('profile.html')


# 修改头像
@user_blueprint.route('profile/', methods=['PATCH'])
def my_profile():
    # 获得头像文件
    avatar = request.files.get('avatar')
    user_id = session.get('user_id')
    if avatar:
        # 保存图片到static/media/xxx.jpg
        avatar.save(os.path.join(UPLOAD_DIR, avatar.filename))
        # 修改数据库相关字段
        user = User.query.get(user_id)
        upload_avatar_path = os.path.join('upload', avatar.filename)
        user.avatar = upload_avatar_path
        user.add_update()
        return jsonify(code=status_code.OK, img_avatar=upload_avatar_path)
    else:
        return jsonify(status_code.USER_PROFILE_AVATAR_IS_NOT_EXISTS)


# 修改用户名
@user_blueprint.route('profile_name/', methods=['PATCH'])
def my_profile_name():
    # 获得头像文件
    name = request.form.get('name')
    user_id = session.get('user_id')
    # 是否输入内容
    if name:
        user = User.query.filter(User.name==name).all()
        # 判断用户名是否已经注册
        if user:
            return jsonify(status_code.USER_REGISTER_USERNAME_IS_EXISTS)
        else:
            user = User.query.get(user_id)
            user.name = name
            user.add_update()
            return jsonify(code=status_code.OK)
    else:
        return jsonify(status_code.USER_REGISTER_PARAMS_NOT_EXISTS)