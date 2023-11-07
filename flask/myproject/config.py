# SQLite
# import os
# BASE_DIR = os.path.dirname(__file__)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# mariadb
db = {
    'user': 'root',
    'password': '12345',
    'host': 'localhost',
    'port': 3306,
    'database': 'flask'
}
# db_url = f"mariadb+mariadbconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

# CSRF방지
SECRET_KEY="dev"
