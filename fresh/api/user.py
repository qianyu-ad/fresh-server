from .base import RestApi, router
from fresh.api.base.parser import admin_parse_form
from fresh.models.user import User
from flask_login import login_user, logout_user, login_required
from fresh.api.base.parser import article_parse_form, page_parse_form, tag_parse_form
from fresh.logger import logger



@router('/api/users')
class UserList(RestApi):

    decorators = [login_required]

    def get(self):
        q = page_parse_form().args()
        users = User.get(
            soft_del=False
        ).paginate(
            q['page'], per_page=q['size'], error_out=False
        )
        return self.ok(users=[u.to_json() for u in users.items])
