from .base import RestApi, router
from flask import request
from flask_restful import reqparse
from fresh.models.topic import (
    db,
    Article,
    Category,
    ReadHistory,
    Like,
    Tag,
    Favorite
)
from fresh.models.user import User
from flask_login import login_required


def parse_form():
    """ 解析表单"""
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    return parser


@router('/api/categories')
class CategoryList(RestApi):
    """ 分类"""

    def get(self):
        categories = Category.get().order_by(
            Category.id
        )
        return self.ok(categories=[c.to_json() for c in categories])

    @login_required
    def post(self):
        data = parse_form().parse_args()
        category = Category.get_first(**data)
        if category:
            return self.no(msg='分类名称已存在')

        category = Category.create(**data)
        if category:
            return self.ok(msg='创建成功')
        else:
            return self.no(msg='创建失败')


@router('/api/categories/<int:c_id>')
class CategoryOne(RestApi):
    """ 分类"""

    decorators = [login_required]

    def post(self, c_id):
        """ 更新"""
        data = parse_form().parse_args()
        category = Category.get_first(**data)
        if category:
            return self.no(msg='分类名称已存在')

        category = Category.get_first(id=c_id)
        if category:
            category.update(name=data['name'])
            return self.ok(msg='更新成功')
        else:
            return self.no(msg='没有找到分类')
    
    def delete(self, c_id):
        """ 删除"""
        category = Category.get_first(id=c_id)
        article_count = Article.get(category_id=c_id, soft_del=False).count()
        if category:
            if article_count > 0:
                return self.no(msg='分类下包含文章无法删除')
            else:
                category.delete(force=True)
                return self.ok(msg='删除成功')
        else:
            return self.no(msg='没有找到分类')


@router('/api/tags')
class TagList(RestApi):
    """ 标签"""

    def get(self):
        tags = Tag.get()
        return self.ok(tags=[t.to_json() for t in tags])
    
    def post(self):
        data = parse_form().parse_args()
        tag = Tag.create(**data)
        if tag:
            return self.ok(msg='创建成功')
        else:
            return self.no(msg='创建失败')



@router('/api/tags/<int:t_id>')
class TagOne(RestApi):

    decorators = [login_required]

    def post(self, t_id):
        data = parse_form().parse_args()
        tag = Tag.get_first(**data)
        if tag:
            return self.no(msg='标签已存在')
        
        tag = Tag.get_first(id=t_id)
        if tag:
            tag.update(**data)
            return self.ok(msg='更新成功')
        else:
            return self.no(msg='没有找到标签')

    def delete(self, t_id):
        tag = Tag.get_first(id=t_id)
        if tag:
            tag.delete(force=True)
            return self.ok(msg='删除成功')
        else:
            return self.no(msg='没有找到标签')