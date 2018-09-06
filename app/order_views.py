from datetime import datetime

from flask import Blueprint, request, session, jsonify, render_template

from app.models import Order, House
from app.user_views import log
from utils import status_code

# 定义蓝图
order_blueprint = Blueprint('order', __name__)


#
@order_blueprint.route('order/', methods=['POST'])
@log
def order():
    # 创建订单模型
    order = Order()
    # 获取开始和结束时间
    begin_date = datetime.strptime(request.form.get('begin_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')

    # 获取当前用户和房屋id
    user_id = session['user_id']
    house_id = request.form.get('house_id')
    # 获取房屋对象
    house = House.query.get(house_id)
    # 写入订单模型数据
    order.user_id = user_id
    order.house_id = house_id
    order.begin_date = begin_date
    order.end_date = end_date
    order.days = (end_date - begin_date).days + 1
    order.house_price = house.price
    order.amount = house.price * order.days
    # 保存模型
    order.add_update()
    return jsonify(status_code.SUCCESS)


# 进入我的订单页面
@order_blueprint.route('orders/', methods=['GET'])
def orders():
    return render_template('orders.html')


# 返回订单信息
@order_blueprint.route('order_info/', methods=['GET'])
@log
def orders_info():
    orders = Order.query.filter(Order.user_id==session['user_id'])
    orders_info = [order.to_dict() for order in orders]
    return  jsonify(orders_info=orders_info, code=status_code.OK)


# 客户定单页面
@order_blueprint.route('lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


# 获得客户订单
@order_blueprint.route('lorder-info', methods=['GET'])
def lorder_info():
    # 获得别人对本人房源下单信息
    # 查询自己的房源信息
    houses = House.query.filter(House.user_id == session['user_id'])
    house_ids = [house.id for house in houses]
    # 查询订单
    lorders = Order.query.filter(Order.house_id.in_(house_ids))
    lorders_info = [order.to_dict() for order in lorders]
    return jsonify(lorders_info=lorders_info, code=status_code.OK)



@order_blueprint.route('o_status/', methods=['PATCH'])
def order_status():
    # 接受订单ID、状态、拒单理由
    # 修改订单
    order_id = request.form.get('order_id')
    status = request.form.get('status')
    comment = request.form.get('comment')
    # 获取订单对象
    order = Order.query.get(order_id)
    order.status = status
    if comment:
        order.comment = comment
    order.add_update()
    return jsonify(status_code.OK)





















































