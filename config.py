import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gsolvit'

    @staticmethod
    def init_app(app):
        pass


config = {
    'default': Config,
    "MYSQL_HOST": '47.104.136.38',
    'MYSQL_PASSWORD': 'root',
    'DATABASE_NAME': 'studenttrainplan2'
}
