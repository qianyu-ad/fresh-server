from flask_restful import reqparse


class BaseParseForm(object):

    def __init__(self):
        self.parser = reqparse.RequestParser()
    
    def merge(self, parser):
        """ 整合不同的 parser"""
        if isinstance(parser, self.__class__):
            parser = parser.parser

        if isinstance(parser, reqparse.RequestParser):
            raise TypeError('Param `parser` is not `RequestParser` instance.')

        for arg in enumerate(self.parser.args[:]):
            for _arg in enumerate(parser.args[:]):
                if arg.name == _arg.name:
                    self.parser.remove_argument(arg.name)
                self.parser.args.append(_arg)
    
    def add(self, name, **kw):
        self.parser.add_argument(name, **kw)
    
    def remove(self, name):
        self.parser.remove_argument(name)
    
    def replace(self, old_name, new_name, **kw):
        self.parser.replace_argument(old_name, new_name, **kw)

    def args(self):
        return self.parser.parse_args()


class ParseForm(BaseParseForm):

    def page_args(self, page=1, size=10):
        """ 分页"""
        self.parser.add_argument('page', default=page, type=int)
        self.parser.add_argument('size', default=size, type=int)


def admin_parse_form():
    """ 管理员登录"""
    parser = ParseForm()
    parser.add('username', required=True)
    parser.add('password', required=True)
    return parser


def tag_parse_form():
    """ 标签"""
    parser = ParseForm()
    parser.add('tagIds', dest='tag_ids')
    return parser


def page_parse_form():
    """ 分页查询"""
    parser = ParseForm()
    parser.page_args()
    return parser


def article_parse_form():
    """ 文章表单"""
    parser = ParseForm()
    parser.add('title', required=True)
    parser.add('content', required=True)
    parser.add('image')
    parser.add('userId', required=True, dest='user_id')
    parser.add('categoryId', required=True, dest='category_id')
    return parser


def reply_parse_form():
    """ 评论表单"""
    parser = ParseForm()
    parser.add('content', required=True)
    parser.add('userId', required=True, dest='user_id')
    parser.add('articleId', required=True, dest='article_id')
    return parser