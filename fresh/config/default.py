"""
项目配置文件
"""
import os
import logging
from kombu import Queue, Exchange

ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
DOWN_DIR = os.path.join(
    ROOT_DIR,
    'downloads',
)

DEBUG = True
SECRET_KEY = b'flask_cap make a project'
REDIS_URL = "redis://localhost:6379/0"
DB_CONFIG = dict(
    host='127.0.0.1',
    db='fresh',
    username='root',
    password='654321',
)

FET_AES_SECRET_KEY = b'fet aes secret key'
SESSION_COOKIE_HTTPONLY = False

# mail 配置
MAIL_SERVER = ''
MAIL_PORT = 25 # 465 sll mode
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''

# celery 配置 -Q `task_name` 指定开启的队列
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERYD_MAX_TASKS_PER_CHILD = 20
CELERYD_TASK_TIME_LIMIT = 60
CELERY_QUEUES = {
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("task_email", Exchange("task_email"), routing_key="task_email"),
}
CELERY_ROUTES = {
    "fresh.tasks.email.send_email": {
        "queue": "task_email",
        "routing_key": "task_email"
    },
}

# 数据库连接
DB_URI = "mysql+pymysql://{}:{}@{}/{}?charset=utf8".format(
    DB_CONFIG['username'], DB_CONFIG['password'],
    DB_CONFIG['host'], DB_CONFIG['db'],
)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True