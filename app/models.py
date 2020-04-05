import datetime
import os
from flask_sqlalchemy import SQLAlchemy
# from app import db
from flask import Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['USER_IMAGE'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/user/')  # 存放用户头像的路径

app.config["SECRET_KEY"] = "543ee8554a184d728183d229c34b8102"
app.debug = True
db = SQLAlchemy(app)


# 定义会员模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    info = db.Column(db.Text)  # 个性简介
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 添加时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符

    def __repr__(self):  # 查询的时候返回
        return "<User %r>" % self.name

    def check_pwd(self, input_pwd):
        """验证密码是否正确，直接将hash密码和输入的密码进行比较，如果相同则，返回True"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, input_pwd)


# 会员日志
class UserLog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 管理员日志
class AdminLog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100))
    admin_id = db.Column(db.Integer)  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class OperateLog(db.Model):
    __tablename__ = "operatelog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer)  # 所属管理员
    ip = db.Column(db.String(100))  # 登录ip
    name = db.Column(db.String(100))
    reason = db.Column(db.String(600))  # 操作原因
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)  # 时间

    def __repr__(self):
        return "Operatelog %r" % self.id


if __name__ == '__main__':
    # 创建数据表
    # print(db)
    #db.create_all()
    #print('创建表')

    from werkzeug.security import generate_password_hash

    user = User(
        name='admin',
        pwd=generate_password_hash('admin')  # 加密密码
    )
    db.session.add(user)
    db.session.commit()