from faker import Faker
from .models import Category, Comment, Post, User
from .extensions import db
import random

fake = Faker()


def fake_categories(count=10):
    category = Category(name='Defalut')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word()[:10])
        db.session.add(category)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()


def fake_post(count=50):
    for i in range(count):
        post = Post(title=fake.sentence()[:10], body=fake.text(2000),
                    timestamp=fake.date_time_this_year(),
                    category=Category.query.get(random.randint(1, Category.query.count())),
                    user=User.query.get(random.randint(1, User.query.count())))
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count())),
            user=User.query.get(random.randint(1, User.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    for i in range(int(0.1 * count)):
        comment = Comment(
            body=fake.sentence(),
            is_root=False,
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count())),
            user=User.query.get(random.randint(1, User.query.count())),
            replied=Comment.query.get(random.randint(1, Comment.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_users(count=10):
    for i in range(count):
        user = User(
            name=fake.name(),
            email=fake.name() + '@example.com',
        )
        user.password = fake.name() + '123'
        db.session.add(user)
    db.session.commit()

