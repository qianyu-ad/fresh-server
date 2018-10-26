"""
应用模块
"""

from fet import _Flask as Flask
from celery import Celery

# pylint: disable=all


celery = Celery(
    __name__,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


def create_app(default='default'):
    """ 创建应用"""
    app = Flask(
        __name__,
    )

    configure_app(app, config_file=default)
    configure_celery_app(app)
    configure_request_hook(app)
    configure_extensions(app)
    configure_blueprints(app)
    return app


def configure_app(app, config_dir="fresh.config", config_file=None):
    """ 基础配置"""
    config_files = ['default']
    if config_file and config_file not in config_files:
        config_files.append(config_file)
    
    for config_file in config_files:
        if config_file.endswith('.py'):
            config_file = config_file[:-3]

        config_path = config_dir + '.' + config_file
        app.config.from_object(config_path)


def configure_celery_app(app):
    """ 配置celery"""
    celery.conf.update(app.config)


def configure_blueprints(app):
    """ 配置蓝图"""
    from fresh.api import bp as api_bp
    from fresh.views.home import bp as home_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(home_bp)


def configure_extensions(app):
    """ 配置扩展"""
    from fresh.extends import (
        api, db, login_manager, mail, redis_store, cryptor
    )
    api.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    redis_store.init_app(app)
    cryptor.init_app(app)


def configure_request_hook(app):
    """ 请求钩子"""

    @app.before_request
    def before_request():
        """ 请求前钩子"""
        pass

    @app.after_request
    def after_request(response):
        """ 请求后钩子"""
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,token' 
        return response