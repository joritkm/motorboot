from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
import os

app = create_app(os.environ.get('FLASK_APP_MODE'))

migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    db.create_all()

if __name__ == '__main__':
    manager.run()
