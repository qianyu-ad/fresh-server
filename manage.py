"""
管理
"""
from flask_script import Server, Manager
from fresh.app import create_app
from fresh.models.user import db, Admin, User
from fresh.models.topic import (
    Category,
    Tag,
    Like,
    ReadHistory,
    Favorite,
    Article,
    ArticleTagRef,
    Reply
)
from flask_migrate import Migrate, MigrateCommand

# pylint: disable=all

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def init_admin():
    # 初始化角色
    admin = Admin.create('admin', 'admin123')
    db.session.add(admin)
    db.session.commit()


@manager.command
def test_data():
    from tests.test_data import test_data
    test_data()


@manager.command
def drop():
    db.drop_all()


@manager.command
def runserver():
    os.system('gunicorn -c unicorn.py manage:app')

manager.add_command('run', Server(
    host='0.0.0.0',
    port=5000,
    use_reloader=True,
    use_debugger=True
))


def main():
    manager.run()

if __name__ == '__main__':
    main()