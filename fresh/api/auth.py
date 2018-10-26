from .base import RestApi, router
from fresh.api.base.parser import admin_parse_form
from fresh.models.user import Admin
from flask_login import login_user, logout_user, login_required
from fresh.logger import logger


@router('/api/admin/login')
class AdminLogin(RestApi):
    
    def post(self):
        data = admin_parse_form().args()
        admin = Admin.authenticate(data['username'], data['password'])
        if admin:
            login_user(admin)
            logger.info('Login User: {}'.format(admin.username))
            return self.ok(msg="成功登录")
        else:
            return self.no(msg="用户名或密码错误")


@router('/api/admin/logout')
class AdminLogout(RestApi):

    decorators = [login_required]

    def get(self):
        logout_user()
        return self.ok(msg='成功退出')