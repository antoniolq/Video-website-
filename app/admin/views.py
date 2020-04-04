from . import admin
from flask import render_template,redirect,url_for,flash,session,request
from app.admin.forms import LoginFrom,PwdForm
from app.models import Admin,Tag,User
from functools import wraps
from app import db, app
import os

def admin_login_require(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('login_admin', None) is None:
            # 如果session中未找到该键，则用户需要登录
            return redirect(url_for('admin.login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

@admin.route("/")
@admin_login_require
def index():
    return render_template("admin/index.html")

@admin.route("/login/", methods=['GET', 'POST'])
def login():
    print("2")
    form = LoginFrom()
    if form.validate_on_submit():
        # 提交的时候验证表单
        data = form.data  # 获取表单的数据
        print(data)
        login_admin = Admin.query.filter_by(name=data['account']).first()
        if not login_admin.check_pwd(data['pwd']):
            # 判断密码错误，然后将错误信息返回，使用flash用于消息闪现
            flash('密码错误！')
            return redirect(url_for('admin.login'))
        # 如果密码正确，session中添加账号记录，然后跳转到request中的next，或者是跳转到后台的首页
        session['login_admin'] = data['account']
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
        admin = Admin.query.filter_by(name=login_name).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data['new_pwd'])
        db.session.commit()  # 提交新密码保存，然后跳转到登录界面
        flash('密码修改成功，请重新登录！', category='ok')
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)


@admin.route("/movie/add/")
@admin_login_require
def movie_add():
    return render_template("/admin/movie_add.html")

@admin.route("/movie/list/")
@admin_login_require
def movie_list():
    return render_template("/admin/movie_list.html")

@admin.route("/preview/add/")
@admin_login_require
def preview_add():
    return render_template("/admin/preview_add.html")

@admin.route("/preview/list/")
@admin_login_require
def preview_list():
    return render_template("/admin/preview_list.html")

@admin.route("/user/list/<int:page>/")
@admin_login_require
def user_list(page=None):
    if page is None:
        page = 1
    page_users = User.query.paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', page_users=page_users)

@admin.route("/user/view/<int:user_id>/")
@admin_login_require
def user_view(user_id=None):
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_view.html', user=user)

@admin.route("/user/add/")
@admin_login_require
def user_add():
    return render_template('admin/user_add.html')

@admin.route("/user/delete/<int:delete_id>/")
@admin_login_require
def user_delete(delete_id=None):
    user = User.query.get_or_404(delete_id)
    # 删除同时要从磁盘中删除封面文件
    file_save_path = app.config['USER_IMAGE']  # 头像上传保存路径
    # 如果存在将进行删除，不判断，如果文件不存在删除会报错
    if os.path.exists(os.path.join(file_save_path, user.face)):
        os.remove(os.path.join(file_save_path, user.face))

    # 删除数据库，提交修改
    db.session.delete(user)
    db.session.commit()
    # 删除后闪现消息
    flash('删除会员成功！', category='ok')
    return redirect(url_for('admin.user_list', page=1))

@admin.route("/comment/list/")
@admin_login_require
def comment_list():
    return render_template("/admin/comment_list.html")

@admin.route("/moviecol/list/")
@admin_login_require
def moviecol_list():
    return render_template("/admin/moviecol_list.html")

@admin.route("/oplog/list/")
@admin_login_require
def oplog_list():
    return render_template("/admin/oplog_list.html")

@admin.route("/adminloginlog/list/")
@admin_login_require
def adminloginlog_list():
    return render_template("/admin/adminloginlog_list.html")

@admin.route("/userloginlog/list/")
@admin_login_require
def userloginlog_list():
    return render_template("/admin/userloginlog_list.html")

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