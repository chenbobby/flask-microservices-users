from flask_script import Manager
from project import app

# Create 'Manager' instance to handle commands in CLI
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
