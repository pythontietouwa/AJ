# author=REI
# date:2019/2/11
from flask import Blueprint, render_template,\
    jsonify,session,request

from app.models import User
from utils.function import login_required

home_blue = Blueprint('home',__name__)



@home_blue.route('/index/',methods=['GET'])
def index():
    return render_template('index.html')