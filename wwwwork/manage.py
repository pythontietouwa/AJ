# author=REI
# date:2019/1/25


from flask import Flask


from flask_script import Manager

from app.home_views import home_blue
from app.models import db
from app.user_view import user_blue

app = Flask(__name__)

app.register_blueprint(blueprint=user_blue,url_prefix='/user')
app.register_blueprint(blueprint=home_blue,url_prefix='/home')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@47.106.215.27:3306/wwwork'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = 'jflwefn23gdf5'
manage = Manager(app)

if __name__ == '__main__':
    manage.run()