# author=REI
# date:2019/2/11
import os
import random
import re
import uuid

from flask import Blueprint, render_template,\
    jsonify,session,request
from sqlalchemy.sql.functions import user

from app.models import User
from utils.function import login_required
user_blue = Blueprint('user',__name__)




@user_blue.route('/register/',methods=['GET'])
def register():
    return render_template('register.html')


@user_blue.route('/register/',methods=['POST'])
def my_register():
    #获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('password')
    passwd2 = request.form.get('password2')
    #1.验证参数是否已填写
    if not all([mobile,imagecode,passwd,passwd2]):
        return jsonify({'code':1001,'msg':'请填写完整的参数'})
    #2.验证手机号正确性
    if not re.match('^1[3456789]\d{9}',mobile):
        return jsonify({'code':1002,'msg':'手机号不正确'})
    #3.验证图片验证码
    if not session['img_code']:
        return jsonify({'code':1003,'msg':'验证码不正确'})
    #4.密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code':1004,'msg':'密码不一致'})
    #验证手机号是否已被注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code':1005,'msg':'手机号已被注册，请重新注册'})
    #创建注册信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code':200,'msg':'请求成功'})


@user_blue.route('/code/',methods=['GET'])
def get_code():
    #获取验证码
    #方式1：后端生成图片，并返回验证码图片的地址(不推荐）
    #方式2：后端只生成一个随机参数，返回给页面，在页面中再生成图片（前端做）
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['img_code'] = code
    return jsonify({'code':200,'msg':'请求成功','data':code})


@user_blue.route('/login/',methods=['GET'])
def login():
    return render_template('login.html')


@user_blue.route('/my_login/',methods=['GET'])
def my_login():
    #实现登录
    phone = request.args.get('phone')
    pwd = request.args.get('pwd')
    #1.校验参数是否填写完成
    if not all([phone,pwd]):
        return jsonify({'code':1006,'msg':'请将请求参数填写完整'})
    #2.获取手机号对应的用户信息
    user = User.query.filter(User.phone == phone).first()
    if not user:
        return jsonify({'code':1007,'msg':'该账号没有注册，可以注册'})
    #3.校验密码是否正确
    if not user.check_pwd(pwd):
        return jsonify({'code':1008,'msg':'密码不正确'})
    #4.登录标识设置
    session['user_id'] = user.id
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/my/',methods=['GET'])
@login_required
def my():
    return render_template('my.html')

@user_blue.route('/user_info/',methods=['GET'])
@login_required
def user_info():
    #获取用户基本信息
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify({'code':200,'msg':'请求成功','data':user.to_basic_dict()})


@user_blue.route('/fix/',methods=['GET'])
@login_required
def fix():
    return render_template('/profile.html')

@user_blue.route('/fix_avatar/',methods=['PATCH'])
@login_required
def fix_avatar():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    avatar = request.files.get('avatar')
    if not all([avatar]):
        return jsonify({'code':1001,'msg':'请选择图片'})
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #获取媒体文件路径
        STATIC_DIR = os.path.join(BASE_DIR,'static')
        MEDIA_DIR = os.path.join(STATIC_DIR,'media')
        filename = str(uuid.uuid4())
        a = avatar.mimetype.split('/')[-1:][0]
        name = filename + '.' + a
        path = os.path.join(MEDIA_DIR,name)
        avatar.save(path)
        user.avatar = name
        user.add_update()
        return jsonify({'code':200})


@user_blue.route('/fix_name/',methods=['PATCH'])
@login_required
def fix_name():
    fix_name = request.form.get('fix_name')
    if fix_name:
        user0 = User.query.filter(User.name==fix_name).first()
        if user0:
            return jsonify({'code':3001,'msg':'用户名已存在，请重新输入'})
        user.name = fix_name
        user.add_update()
        return jsonify({'code':200,'msg':'修改成功'})


@user_blue.route('/auth/',methods=['GET'])
@login_required
def auth1():
    return render_template('auth.html')


@user_blue.route('/auth/',methods=['POST'])
@login_required
def auth():
    read_name = request.form.get('id_name')
    id_card = request.form.get('id_card')
    if not all([read_name,id_card]):
        return jsonify({'code':1001,'msg':'填入信息不完全'})
    if not re.match(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
        return jsonify({'code':1002,'msg':'身份填写不合格'})

    user = User.query.get(session['user_id'])
    user.read_name = read_name
    user.id_card = id_card
    try:
        user.add_update()
        return jsonify({'code':202,'msg':'上传成功'})
    except Exception as e:
        print(e)
        return jsonify({'code':1001,'msg':'上传失败'})


@user_blue.route('/myhouse/',methods=['GET'])
@login_required
def myhouse():
    return render_template('myhouse.html')


@user_blue.route('/newhouse/',methods=['GET'])
@login_required
def newhouse():
    return render_template('newhouse.html')


@user_blue.route('/orders/',methods=['GET'])
@login_required
def orders():
    return render_template('orders.html')


@user_blue.route('/lorders/',methods=['GET'])
@login_required
def lorders():
    return render_template('lorders.html')