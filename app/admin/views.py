from . import admin
from flask import render_template,redirect,url_for,flash,session,request
from app.admin.forms import LoginFrom,PwdForm,RegisterForm
from app.models import User,AdminLog,OperateLog
from functools import wraps
from app import db
from werkzeug.security import generate_password_hash
import datetime
import uuid

import os

def admin_login_require(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('login_admin', None) is None:
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
            flash('密码错误！')
            return redirect(url_for('admin.login'))
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
        db.session.commit()
        opLogRecord(session['login_admin'], "修改密码")
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


@admin.route("/userloginlog/list/<int:page>/")
@admin_login_require
def userloginlog_list(page=None):
    opLogRecord(session['login_admin'], "查看登录日志")
    if not page:
        page = 1
    print(session)
    page_user_logs = AdminLog.query.order_by(
        AdminLog.add_time.desc()
    ).paginate(page=page, per_page=10)
    print(page_user_logs)
    return render_template("/admin/userloginlog_list.html",page_user_logs=page_user_logs)




