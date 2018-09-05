import os
import random
import re
from functools import wraps

from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for

from app.models import db, User, House, Area, Facility, HouseImage
from utils import status_code


# 定义蓝图
from utils.setting import UPLOAD_DIR

house_blueprint = Blueprint('house', __name__)


# 定义一个修饰器用来审查cookie中的session_id
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = session.get('user_id')
        if user is None:
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return wrapper


# 进入我的房源
@house_blueprint.route('my_house/', methods=['GET'])
def my_house():
    return render_template('myhouse.html')


# 判断是否实名认证
@house_blueprint.route('house_info/', methods=['GET'])
@log
def house_info():
    # 判断当前登录系统的用户是否实名认证，如果实名认证，返回该用户发布的房屋信息
    user = User.query.get(session['user_id'])
    if user.id_card:
        # 已经实名认证了，返回房屋信息
        houses = House.query.filter(House.user_id == session['user_id']).all()
        house_info = [house.to_dict()for house in houses]
        return jsonify(code=status_code.OK,house_info=house_info)
    else:
        return jsonify(status_code.HOUSE_MYHOUSE_NAME_IS_NOT_VALID)


# 发布房源
@house_blueprint.route('newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


@house_blueprint.route('area_facility/',methods=['GET'])
def area_facility():
    # 获取所有区域
    areas=Area.query.all()
    # 获得所有设备
    facilities=Facility.query.all()
    # 将设施和区域序列化
    area_info=[area.to_dict()for area in areas]
    facility_info=[facility.to_dict()for facility in facilities]
    return jsonify(code=status_code.OK,area_info=area_info,facilities_info=facility_info)


# 创建房源
@house_blueprint.route('newhouse/', methods=['POST'])
def my_new_house():
    data = request.form
    house = House()
    house.user_id = session['user_id']
    house.title = data.get('title')
    house.price = data.get('price')
    house.area_id = data.get('area_id')
    house.address = data.get('address')
    house.room_count = data.get('room_count')
    house.acreage = data.get('acreage')
    house.unit = data.get('unit')
    house.capacity = data.get('capacity')
    house.beds = data.get('beds')
    house.deposit = data.get('deposit')
    house.min_days = data.get('min_days')
    house.max_days = data.get('max_days')
    # 获取设施列表， 使用getlist
    facilities =data.getlist('facility')
    for f_id in facilities:
        facility = Facility.query.get(f_id)
        # 添加房屋和设施的关联关系，多对多
        house.facilities.append(facility)
    house.add_update()
    house_id = house.id
    return jsonify({'house_id': house_id, 'code': 200 })


# 创建房源图片
@house_blueprint.route('newhouse_img/', methods=['POST'])
def new_house_img():
    # 获得图片
    img = request.files.get('house_image')
    house_id = request.form.get('house_id')
    # 获得房屋
    house = House.query.get(house_id)
    # 保存图片到文件夹
    img.save(os.path.join(UPLOAD_DIR, img.filename))
    # 保存房屋图片信息
    image_url = os.path.join('upload', img.filename)
    # 保存房屋的首图
    if not house.index_image_url:
        house.index_image_url = image_url
        house.add_update()
    # 创建一个中间表对象
    h_image = HouseImage()
    h_image.house_id = house_id
    h_image.url = image_url
    h_image.add_update()
    return jsonify(code=status_code.OK, image_url=image_url)
