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
from fresh.api.parser import ParseFrom


def parse_form():
    """ 解析表单"""
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    return parser


@router('/api/categoies')
class CategoryList(RestApi):
    """ 分类"""

    def get(self):
        categories = Category.get()
        return self.ok(categories=[c.to_json() for c in categories])

    def post(self):
        data = parse_form().parse_args()
        category = Category.create(**data)
        if category:
            return self.ok(msg='创建成功')
        else:
            return self.no(msg='创建失败')


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
