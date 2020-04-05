#coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin,User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp

class LoginFrom(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号！')
        ],
        description='账号',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入账号",
            'required': "required"
        }
    )

    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！')
        ],
        description='密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入密码",
            'required': "required"
        }
    )
    submit = SubmitField(
        label='登录',
        render_kw={
            'class': "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self, field):
        """从Admin数据库中，检测账号是否存在，如果不存在则在account.errors中添加错误信息"""
        account = field.data
        admin_num = User.query.filter_by(name=account).count()
        if admin_num == 0:
            raise ValidationError('账号不存在')

class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码！')
        ],
        description='旧密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入旧密码",
            'required': "required"
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码！')
        ],
        description='新密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入新密码",
            'required': "required"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )

    def validate_old_pwd(self, field):
        """检查验证旧密码是否正确"""
        from flask import session
        old_pwd = field.data
        login_name = session['login_admin']
        admin = Admin.query.filter_by(name=login_name).first()
        if not admin.check_pwd(old_pwd):
            raise ValidationError('旧密码错误！')

class RegisterForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired('请输入昵称！')
        ],
        description='昵称',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入昵称",
            'required': "required",
            'autofocus': "autofocus"
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱！'),
            Email('邮箱格式不正确')
        ],
        description='邮箱',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入邮箱",
            'required': "required",
            'autofocus': "autofocus"
        }
    )
    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请输入手机！'),
            Regexp('^1[3|4|5|6|7|8][0-9]\d{4,8}$', message='手机格式不正确')
        ],
        description='手机',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入手机",
            'required': "required",
            'autofocus': "autofocus"
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！')
        ],
        description='密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入密码",
            'required': "required"
        }
    )
    repwd = PasswordField(
        label='重复密码',
        validators=[
            DataRequired('请输入重复密码！'),
            EqualTo('pwd', message='两次密码不一致')
        ],
        description='重复密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入重复密码",
            'required': "required"
        }
    )
    face = FileField(
        label='头像',
        validators=[
            DataRequired('请上传头像')
        ],
        description='头像',
    )
    submit = SubmitField(
        label='添加',
        render_kw={
            'class': "btn btn-primary"
        }
    )
