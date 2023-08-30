import os
import unittest
import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main.model.user import User
from app.main.model.authority import Authority
from app.main.model.user_group import User_group
from app import blueprint
from app.main import create_app, db

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@app.before_first_request
def insert_initial_data():
    if not Authority.query.first():
        Top_manager = Authority(
            authority_context='Top Manager Authority'
        )
        db.session.add(Top_manager)
        db.session.commit()

    if not User_group.query.first():
        group_authority = Authority.query.filter(
            Authority.authority_context == 'Top Manager Authority'
        ).first()
        Top_manager_group = User_group(
            user_group_name='Top Manager Group',
            group_authority=group_authority.authority_key
        )
        db.session.add(Top_manager_group)
        db.session.commit()

    if not User.query.first():
        Top_manager_group_number = User_group.query.filter(
            User_group.user_group_name == 'Top Manager Group'
        ).first()
        admin = User(
            student_id='111111111',
            username='Top Manager',
            password='1111',
            user_group=Top_manager_group_number.user_group_key,
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(admin)
        db.session.commit()


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
