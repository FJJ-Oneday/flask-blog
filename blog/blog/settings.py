import os


class BaseConfig:

    SECRET_KEY = os.urandom(16)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEFAULT_PER_PAGE = 10

    CKEDITOR_FILE_UPLOADER = 'admin.upload'
    CKEDITOR_ENABLE_CSRF = True

    BASE_FILE_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEVELOPMENT_DATABASE_URL',
                                             'mysql://root:root@localhost/flask')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')


config = {
    'default': BaseConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}