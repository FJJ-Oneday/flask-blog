import os

from flask import Blueprint, render_template, \
    redirect, url_for, flash, send_from_directory, request, current_app
from flask_ckeditor import upload_fail, upload_success
from flask_login import login_required, current_user

from ..extensions import db
from ..forms import CommentForm, PostForm
from ..models import Comment, Post, Category

admin = Blueprint('admin', __name__)


@admin.before_request
@login_required
def login_protect():
    pass


@admin.route('/add_comment', methods=['POST'])
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        body = form.comment.data
        is_root = True if form.comment_root.data == 'true' else False
        replied = None
        if not is_root:
            replied = Comment.query.get(int(form.comment_root.data))
        comment = Comment(body=body,
                          is_root=is_root,
                          replied=replied,
                          user=current_user,
                          post=Post.query.get(int(form.post_id.data)))
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blog.post_details',
                                post_id=int(form.post_id.data)) + '#comment-%s' % form.comment_root.data)

    return redirect(url_for('blog.post_details', post_id=int(form.post_id.data)) + '#comment-part')


@admin.route('/board')
def board():
    posts = Post.query.with_parent(current_user).order_by(Post.timestamp.desc()).all()
    return render_template('admin/admin.html', posts=posts)


@admin.route('/files/<path:filename>')
def uploaded_files(filename):
    path = current_app.config.get('BASE_FILE_FOLDER')
    return send_from_directory(path, filename)


@admin.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(current_app.config.get('BASE_FILE_FOLDER'), f.filename))
    url = url_for('admin.uploaded_files', filename=f.filename)
    return upload_success(url=url)  # return upload_success call


@admin.route('/new_post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data,
        body = form.body.data,
        category = Category.query.get(form.category.data)
        post = Post(
            title=title,
            body=body,
            category=category,
            user=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('保存成功.')
    return render_template('admin/edit_post.html', form=form)


@admin.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get(post_id)
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = form.category.data
        post.title = title
        post.category = Category.query.get(category)
        post.body = body

        db.session.commit()

        flash('保存成功.')

    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category.id
    return render_template('admin/edit_post.html', form=form)


@admin.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('删除成功.')
    return redirect(request.args.get('next'))


@admin.route('/posts/comments')
def comment_info():
    posts = Post.query.with_parent(current_user).all()
    return render_template('admin/comment_info.html', posts=posts)


@admin.route('/<int:post_id>/comments')
def manage_comment(post_id):
    comments = Comment.query.with_parent(Post.query.get_or_404(post_id)).all()
    return render_template('admin/comment_details.html', comments=comments)


@admin.route('/comment/<int:comment_id>/view', methods=['POST'])
def view_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.is_reviewed = True
    db.session.commit()
    return redirect(request.args.get('next'))


@admin.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('删除成功')
    return redirect(request.args.get('next'))


@admin.route('/search', methods=['POST', 'GET'])
def search():
    search_key = request.form['search_key'].strip()
    posts = Post.query.with_parent(current_user) \
        .filter(Post.title.like('%{}%'.format(search_key))).all()
    return render_template('admin/admin.html', posts=posts)
