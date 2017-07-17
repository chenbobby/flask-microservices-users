# manage.py

import unittest
from flask_script import Manager
import coverage

from project import create_app, db
from project.api.models import User


# Activate coverage reports
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*'
    ]
)
COV.start()


# Create Flask app from factory
app = create_app()

# Create 'Manager' instance to handle commands in CLI
manager = Manager(app)


@manager.command
def test():
    """Runs tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs unit tests with coverage report."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def recreate_db():
    """Clears and Recreates database"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """Seeds database with initial data"""
    db.session.add(User(username='test1', email='test1@example.com'))
    db.session.add(User(username='test2', email='test2@example.com'))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
