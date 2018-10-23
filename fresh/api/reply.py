
from .base import RestApi, router
from flask import request
from fresh.models.topic import db, Like, Reply
from fresh.models.user import User
from fresh.api.base.parser import page_parse_form, reply_parse_form
from fresh.utils import fmt_datetime as fmt_dt


class ReplyResponse(object):

    @classmethod
    def json(self, replies):
        ids = [r.id for r in replies]
        user_ids = [r.user_id for r in replies]
        users = User.query.filter(User.id.in_(user_ids))
        likes = Like.query.filter(Like.type == Like.TYPE_REPLY, Like.m_id.in_(ids))
        result = []
        for reply in replies:
            user = users.filter(User.id == reply.user_id).first()
            like_count = likes.filter(Like.m_id == reply.id).count()
            result.append({
                'id': reply.id,
                'content': reply.content,
                'likes': like_count,
                'user': {
                    'id': user.id,
                    'name': user.name,
                },
                'createTime': fmt_dt(reply.create_time),
                'updateTime': fmt_dt(reply.update_time),
            })
        return result


@router('/api/replies')
class ReplyList(RestApi):
    """ 评论"""

    def get(self):
        replies = Reply.get(soft_del=False)
        return self.ok(replies=ReplyResponse.json(replies))

    def post(self):
        data = reply_parse_form().args()
        reply = Reply.create(**data)
        if reply:
            return self.ok(msg='创建成功')
        else:
            return self.no(msg='创建失败')


@router('/api/replies/<int:reply_id>')
class ReplyOne(RestApi):
    pass