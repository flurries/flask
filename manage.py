from flask_script import Manager

from utils.app import cerate_app

app = cerate_app()

manage = Manager(app=app)

if __name__ == '__main__':
    manage.run()