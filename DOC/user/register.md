## register
####POST   /user/register/
    -  参数
        - mobile        手机号
        - imagecode     图片验证码
        - passwd        密码
        - passwd2       确认密码
     - 响应
        - {'code': 1000, 'msg': '请填写完整的参数'}
        - {'code': 1001, 'msg': '手机号不符合规范'}
        - {'code': 1002, 'msg': '图片验证码错误'}
        - {'code': 1003, 'msg': '密码不一致'}
        - {'code': 1004, 'msg': '该手机号已注册，请去登陆'}