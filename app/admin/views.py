from . import admin
from flask import render_template,redirect,url_for,flash,session,request
from app.admin.forms import LoginFrom,PwdForm,RegisterForm
from app.models import Admin,Tag,User,UserLog,AdminLog,OperateLog
from functools import wraps
from app import db, app
from werkzeug.security import generate_password_hash
import datetime
import uuid

import os

def admin_login_require(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('login_admin', None) is None:
            # 如果session中未找到该键，则用户需要登录
            return redirect(url_for('admin.login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

def loginLogRecord(str):
    adminlog = AdminLog(
        name=str,
        ip='127.0.0.1',
        add_time = datetime.datetime.now()
    )
    db.session.add(adminlog)
    db.session.commit()

def opLogRecord(name,reason):
    operateLog = OperateLog(
        name=name,
        ip='127.0.0.1',
        reason=reason,
        add_time = datetime.datetime.now()
    )
    db.session.add(operateLog)
    db.session.commit()

@admin.route("/")
@admin_login_require
def index():
    return render_template("admin/index.html")

@admin.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        data = form.data  # 获取表单的数据
        login_admin = User.query.filter_by(name=data['account']).first()
        if not login_admin.check_pwd(data['pwd']):
            # 判断密码错误，然后将错误信息返回，使用flash用于消息闪现
            flash('密码错误！')
            return redirect(url_for('admin.login'))
        # 如果密码正确，session中添加账号记录，然后跳转到request中的next，或者是跳转到后台的首页
        session['login_admin'] = data['account']
        loginLogRecord(data['account'])
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)

@admin.route("/logout/")
def logout():
    session.pop('login_admin', None)  # 删除session中的登录账号
    return redirect(url_for("admin.login"))

@admin.route("/pwd/", methods=['GET', 'POST'])
@admin_login_require
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        login_name = session['login_admin']
        admin = User.query.filter_by(name=login_name).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data['new_pwd'])
        db.session.commit()  # 提交新密码保存，然后跳转到登录界面
        flash('密码修改成功，请重新登录！', category='ok')
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)


@admin.route("/video/track/")
@admin_login_require
def video_track():
    opLogRecord(session['login_admin'], "查看人体跟踪算法效果")
    return render_template("/admin/video_track.html")

@admin.route("/video/action/")
@admin_login_require
def video_action():
    opLogRecord(session['login_admin'], "查看行为识别算法效果")
    return render_template("/admin/video_action.html")


@admin.route("/user/list/<int:page>/")
@admin_login_require
def user_list(page=None):
    opLogRecord(session['login_admin'], "查看用户列表")
    if page is None:
        page = 1
    page_users = User.query.paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', page_users=page_users)

@admin.route("/user/view/<int:user_id>/")
@admin_login_require
def user_view(user_id=None):
    opLogRecord(session['login_admin'], "查看用户详情")
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_view.html', user=user)

@admin.route("/user/add/", methods=['GET', 'POST'])
@admin_login_require
def user_add():
    opLogRecord(session['login_admin'], "添加用户")
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            email=data['email'],
            phone=data['phone'],
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('添加用户成功！', category='ok')
        return redirect(url_for('admin.user_add'))
    return render_template('admin/user_add.html', form=form)


@admin.route("/oplog/list/<int:page>")
@admin_login_require
def oplog_list(page=None):
    opLogRecord(session['login_admin'], "查看操作日志")
    if not page:
        page = 1
    print(session)
    page_op_logs = OperateLog.query.order_by(
        OperateLog.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template("/admin/oplog_list.html", page_op_logs=page_op_logs)

@admin.route("/adminloginlog/list/")
@admin_login_require
def adminloginlog_list():
    return render_template("/admin/adminloginlog_list.html")

@admin.route("/userloginlog/list/<int:page>/")
@admin_login_require
def userloginlog_list(page=None):
    """会员登录日志"""
    opLogRecord(session['login_admin'], "查看登录日志")
    if not page:
        page = 1
    print(session)
    page_user_logs = AdminLog.query.order_by(
        AdminLog.add_time.desc()
    ).paginate(page=page, per_page=10)
    print(page_user_logs)
    return render_template("/admin/userloginlog_list.html",page_user_logs=page_user_logs)

@admin.route("/role/add/")
@admin_login_require
def role_add():
    return render_template("/admin/role_add.html")

@admin.route("/role/list/")
@admin_login_require
def role_list():
    return render_template("/admin/role_list.html")

@admin.route("/auth/add/")
@admin_login_require
def auth_add():
    return render_template("/admin/auth_add.html")

@admin.route("/auth/list/")
@admin_login_require
def auth_list():
    return render_template("/admin/auth_list.html")

@admin.route("/admin/add/")
@admin_login_require
def admin_add():
    return render_template("/admin/admin_add.html")

@admin.route("/admin/list/")
@admin_login_require
def admin_list():
    return render_template("/admin/admin_list.html")