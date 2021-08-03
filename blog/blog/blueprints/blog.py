from flask import Blueprint, render_template, request, current_app

from ..models import Post, Category
from ..forms import CommentForm

blog = Blueprint('blog', __name__)


@blog.route('/', defaults={'page': 1})
@blog.route('/index/<int:page>')
def index(page):
    per_page = current_app.config.get('DEFAULT_PER_PAGE')
    pagination = Post.query.order_by(Post.timestamp.desc()) \
        .paginate(page, per_page=per_page)
    posts = pagination.items
    # categories = Category.query.all()
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog.route('/post/<int:post_id>')
def post_details(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)
    return render_template('blog/post.html', post=post, form=form)


@blog.route('/cagegory/<int:category_id>')
def category(category_id):
    category = Category.query.get(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('DEFAULT_PER_PAGE')
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc())\
        .paginate(page, per_page=per_page)
    posts = pagination.items

    return render_template('blog/category.html', pagination=pagination, posts=posts, category=category)


@blog.route('/search')
def search():
    pass
