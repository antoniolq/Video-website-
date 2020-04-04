#coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin


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
        admin_num = Admin.query.filter_by(name=account).count()
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