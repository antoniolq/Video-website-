from . import admin
from flask import render_template,redirect,url_for,flash,session,request
from app.admin.forms import LoginFrom,TagForm
from app.admin.forms import LoginFrom,TagForm
from app.models import Admin,Tag
from functools import wraps
from app import db

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

@admin.route("/pwd/")
@admin_login_require
def pwd():
    return render_template("admin/pwd.html")

@admin.route("/tag/add/",methods=["GET","POST"])
@admin_login_require
#TODO
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name = data["name"]).count()
        if tag == 1:
            flash("名称已存在！","err")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加成功！","ok")
        redirect(url_for('admin.tag_add'))
    return render_template("/admin/tag_add.html",form=form)

@admin.route("/tag/list/<int:page>/", methods=["GET"])
@admin_login_require
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.add_time.desc()
    ).paginate(page=page,per_page=10)
    return render_template("/admin/tag_list.html",page_data=page_data)

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

@admin.route("/user/list/")
@admin_login_require
def user_list():
    return render_template("/admin/user_list.html")

@admin.route("/user/view/")
@admin_login_require
def user_view():
    return render_template("/admin/user_view.html")

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