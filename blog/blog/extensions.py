from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager
from flask_avatars import Avatars
from flask_wtf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
moment = Moment()
login_manager = LoginManager()
avatars = Avatars()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)


login_manager.login_view = 'auth.login'
