from .base import RestApi, router
from flask import request
from flask_restful import reqparse
from fresh.models.topic import (
    db,
    Article,
    Category,
    ReadHistory,
    Like,
    Favorite,
    Tag,
    ArticleTagRef
)
from fresh.models.user import User
from fresh.api.base.parser import article_parse_form, page_parse_form, tag_parse_form
from fresh.utils import fmt_datetime as fmt_dt
from fresh.logger import logger


class ArticleResponse(object):
    """ 格式化文章返回值"""

    @classmethod
    def get_tag_map(cls, article_ids):
        refs = ArticleTagRef.query.filter(ArticleTagRef.article_id.in_(article_ids))
        tag_ids = [r.tag_id for r in refs]
        tags = Tag.query.filter(Tag.id.in_(tag_ids))
        result = {}
        for article_id in article_ids:
            _refs = refs.filter(ArticleTagRef.article_id == article_id)
            _tag_ids = [r.tag_id for r in _refs]
            result[article_id] = tags.filter(ArticleTagRef.tag_id.in_(_tag_ids))
        return result


    @classmethod
    def json(cls, articles):
        ids = [article.id for article in articles]
        user_ids = [article.user_id for article in articles]
        category_ids = [article.category_id for article in articles]

        users = User.query.filter(User.id.in_(user_ids))
        categories = Category.query.filter(Category.id.in_(category_ids))
        likes = Like.query.filter(Like.m_id.in_(ids), Like.type == Like.TYPE_ARTICLE)
        read_histories = ReadHistory.query.filter(ReadHistory.article_id.in_(ids))
        tag_list = cls.get_tag_map(ids)

        result = []
        for article in articles:
            user = users.filter(User.id == article.user_id).first()
            category = categories.filter(Category.id == article.category_id).first()
            tags = tag_list[article.id]
            like_count = likes.filter(Like.m_id == article.id).count()
            reads = read_histories.filter(ReadHistory.article_id == article.id)
            read_count = reads.count()
            click_count = sum([r.count for r in reads])
            result.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'image': article.image,
                'createTime': fmt_dt(article.create_time),
                'updateTime': fmt_dt(article.update_time),
                'user': {
                    'id': user.id,
                    'name': user.name,
                },
                'category': {
                    'id': category.id,
                    'name': category.name,
                },
                'status': article.status,
                'likes': like_count,
                'reads': read_count,
                'clicks': click_count,
                'tags': [t.to_json() for t in tags]
            })
        return result


@router('/api/articles')
class ArticleList(RestApi):
    """ 文章列表"""

    def get(self):
        """ 获取文章列表"""
        q = page_parse_form().args()
        articles = Article.get(
            soft_del=False
        ).paginate(
            q['page'], per_page=q['size'], error_out=False
        )
        return self.ok(
            articles=ArticleResponse.json(articles.items)
        )

    def post(self):
        """ 创建文章"""
        data = article_parse_form().args()
        article = Article.create(**data)
        if article:
            tag_ids = tag_parse_form().args()['tag_ids']
            tag_ids = [tag.strip() for tag in tag_ids.split(',') if tag]
            refs = [{'tag_id': tag_id, 'article_id': article.id} for tag_id in tag_ids]
            db.session.bulk_insert_mappings(
                ArticleTagRef, refs,
            )
            db.session.commit()
            return self.ok(msg='创建成功')
        else:
            return self.no(msg='创建失败')


@router('/api/articles/<int:article_id>')
class ArticleOne(RestApi):
    """ 文章"""

    def get(self, article_id):
        article = Article.get_first(id=article_id)
        if article:
            user_id = request.args.get('user_id')
            if user_id:
                # 如果存在user_id表示用户浏览，添加记录
                ReadHistory.create_or_update(user_id, article.id)
            return self.ok(article=article.to_json())
        else:
            return self.no(msg="没有找到该文章")

    def post(self, article_id):
        parser = article_parse_form()
        parser.remove('user_id')
        data = parser.args()

        article = Article.get_first(id=article)
        if article:
            article.update(**data)
            return self.ok(msg="更新成功")
        else:
            return self.no(msg="没有找到该文章")


@router('/api/articles/<int:article_id>/status')
class ArticleStatus(RestApi):
    """ 文章状态"""

    def post(self, article_id):
        try:
            status = request.args.get('status', type=int)
        except ValueError:
            return self.no(msg="无效的状态")

        article = Article.get_first(id=article_id)
        if article:
            if status > -1 and status < 3:
                article.update(status=status)
                return self.ok(msg="更新成功")
            else:
                return self.no(msg="无效的状态")
        else:
            return self.no(msg="没有找到该文章")


@router('/api/articles/<int:article_id>/favorite')
class ArticleFavorite(RestApi):
    """ 收藏"""

    def post(self, article_id):
        user_id = request.args.get('user_id')

        if not user_id:
            return self.no(msg='无效的用户id')

        Favorite.create_or_update(user_id, article_id)
        return self.ok(msg='ok')