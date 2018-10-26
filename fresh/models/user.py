"""
数据模型
"""

from datetime import datetime
from flask import jsonify
from flask_login import UserMixin
from fresh.extends import db, login_manager, cryptor
from fresh.utils import get_code
from fresh.mixins.crud import CRUDMixin

# pylint: disable=all


class Admin(db.Model, UserMixin):
    """ 用户"""

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    soft_del = db.Column(db.Boolean, default=False)

    def __init__(self, username, password):
        """ 初始化"""
        self.username = username
        self.password = password

    @classmethod
    def create(cls, username, password):
        """ 创建用户"""
        admin = cls(username, password)
        db.session.add(admin)
        db.session.commit()
        return admin

    @property
    def password(self):
        """ 获取密码hash值"""
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        """ 设置密码"""
        salt = get_code()
        self.salt = salt
        self.password_hash = cryptor.encrypt(password, salt=salt)

    def verify_password(self, password):
        """ 验证密码"""
        return self.password_hash == cryptor.encrypt(password, salt=self.salt)

    @classmethod
    def authenticate(cls, username, password):
        """ 验证"""
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.verify_password(password):
            return admin

    def __repr__(self):
        return '<Admin id: {}, username: {}>'.format(self.id, self.username)


class User(db.Model, CRUDMixin):
    """ 微信用户
    :field id: 微信openid
    :field name: 微信名称
    :field avatar_url: 微信头像
    :field gender: 性别
    :field country: 微信用户所在国家
    :field province: 微信用户所在省份
    :field city: 微信用户所在城市
    """
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    avatar_url = db.Column(db.String(400))
    gender = db.Column(db.Integer, default=1)
    country = db.Column(db.String(50), default='')
    province = db.Column(db.String(50), default='')
    city = db.Column(db.String(50), default='')
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    last_login_time = db.Column(db.DateTime, default=datetime.now)
    soft_del = db.Column(db.Boolean, default=False)


@login_manager.user_loader
def load_user(admin_id):
    """ 获取登录用户"""
    admin = Admin.query.filter_by(id=admin_id).first()
    return admin


# @login_manager.unauthorized_handler
# def unauthenticated():
#     """ 用户未登录"""
#     return jsonify({
#         'code': 0,
#         'msg': '用户没有登录',
#     })