# coding=utf8

from datetime import datetime
from sqlalchemy.databases import mysql
from fresh.extends import db
from fresh.mixins.crud import CRUDMixin
from fresh.models.user import User
from fresh.utils import fmt_datetime as fmt_dt

# pylint: disable=all


class Category(db.Model, CRUDMixin):
    """ 分类"""

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Tag(db.Model, CRUDMixin):
    """ 标签"""

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Like(db.Model, CRUDMixin):
    """ 点赞
    :field user_id: 点赞用户
    :field o_id: 模块的id
    :field type: 模块的类型（文章或这评论）
    """

    TYPE_ARTICLE = 'Article'
    TYPE_REPLY = 'Reply'

    __tablename__ = 'likes'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    m_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    soft_del = db.Column(db.Boolean, default=False)


class ReadHistory(db.Model, CRUDMixin):
    """ 阅读历史"""

    __tablename__ = 'rd_history'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    article_id = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, default=0)

    @classmethod
    def create_or_update(cls, user_id, article_id):
        """ 创建或更新"""
        item = cls.get_first(user_id=user_id, article_id=article_id)
        if item:
            try:
                item.count += 1
                db.session.commit()
            except:
                db.session.rollback()
        else:
            cls.create(user_id=user_id, article_id=article_id)


class Favorite(db.Model, CRUDMixin):
    """ 用户收藏"""

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    article_id = db.Column(db.Integer, nullable=False)
    soft_del = db.Column(db.Boolean, default=False)

    @classmethod
    def create_or_update(cls, user_id, article_id):
        """ 创建胡更新"""
        item = cls.get_first(user_id=user_id, article_id=article_id)
        if item:
            item.delete()
        else:
            item.create(user_id=user_id, article_id=article_id)


class ArticleTagRef(db.Model, CRUDMixin):
    """ 文章标签关联表"""
    __tablename__ = 'article_tag_ref'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, nullable=False)
    tag_id = db.Column(db.Integer, nullable=False)


class ArticleStatus(object):
    """ 文章状态
    :param check: 检测
    :param online: 上线
    :param offline: 下线
    """
    CHECK = 0
    ONLINE = 1
    OFFLINE = 2


class Article(db.Model, CRUDMixin, ArticleStatus):
    """ 用户发表文章
    :field user_id: 微信openid
    :field category_id: 分类id
    :field title: 文章标题
    :field content: 文章内容
    :field image: 图片Url
    :field status: 文章状态
    """

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(mysql.MEDIUMTEXT, nullable=False)
    image = db.Column(db.TEXT)
    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    soft_del = db.Column(db.Boolean, default=False)

    def to_json(self):
        user = User.get_first(id=self.user_id)
        category = Category.get_first(id=self.category_id)
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'image': self.image,
            'createTime': fmt_dt(self.create_time),
            'updateTime': fmt_dt(self.update_time),
            'user': {
                'id': user.id,
                'name': user.name,
            },
            'category': {
                'id': category.id,
                'name': category.name,
            }
        }


class Reply(db.Model, CRUDMixin):
    """ 用户评论"""

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    article_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    soft_del = db.Column(db.Boolean, default=False)
