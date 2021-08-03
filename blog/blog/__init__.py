from flask import Flask

from .blueprints.admin import admin
from .blueprints.auth import auth
from .blueprints.blog import blog
from .extensions import *
from .settings import config
from .models import *
import click


def create_app(config_name=None):
    if config_name is None:
        config_name = 'development'

    app = Flask('blog')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commends(app)
    register_template_context(app)
    register_shell_context(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ckeditor.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    avatars.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog)
    app.register_blueprint(admin, url_prefix='/user')
    app.register_blueprint(auth, url_prefix='/auth')


def register_commends(app: Flask):
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--email', prompt=True)
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
                  help='The password used to login.')
    def init(username, email, password):
        click.echo('Initializing the database')
        db.create_all()

        user = User.query.filter_by(name=username).first()
        if user:
            click.echo('user already exits.')
        else:
            user = User(name=username, email=email)
            user.password = password
            db.session.add(user)
            db.session.commit()
            click.echo('Done.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of categories, default is 10.')
    @click.option('--comment', default=500, help='Quantity of categories, default is 10.')
    def forge(category, post, comment):
        from .fakes import fake_post, fake_comments, fake_categories, fake_users

        db.drop_all()
        db.create_all()

        click.echo('Generating the users')
        fake_users()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_post(post)

        click.echo('Generation %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')


def register_shell_context(app):
    @app.shell_context_processor
    def shell_context():
        return dict(db=db, User=User, Comment=Comment)


def register_template_context(app):
    @app.context_processor
    def template_context():
        categories = Category.query.all()
        return dict(categories=categories)
