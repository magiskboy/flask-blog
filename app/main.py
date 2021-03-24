import os
import secrets

from PIL import Image
from flask import (
    request,
    render_template,
    url_for,
    flash,
    redirect,
    abort,
    Blueprint,
    current_app,
)
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
)

from .forms import (
    LoginForm,
    RegistrationForm,
    UpdateAccountForm,
    PostForm,
)
from .models import (
    User,
    Post,
)


bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    template = 'main/home.html'
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template(template, posts=posts)


@bp.route('/about')
def about():
    template = 'main/about.html'
    return render_template(template, title='About')


@bp.route('/register', methods=['POST', 'GET'])
def register():
    template = 'main/register.html'
    form = RegistrationForm()
    context = {
        'title': 'Register',
        'form': form,
    }

    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.password = form.password.data
        user.save()
        flash(f'Your account have been created! You are now able to login', 'success')
        return redirect(url_for('main.home'))

    return render_template(template, **context)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    template = 'main/login.html'
    form = LoginForm()
    context = {
        'title': 'Login',
        'form': form,
    }
    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login Unsuccessful. Please check email or password', 'danger')
    return render_template(template, **context)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/main/profile_pics', picture_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    template = 'main/account.html'
    form = UpdateAccountForm()
    context = {
        'title': 'Account',
        'form': form,
    }
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.save()
        flash('You account have been updated', 'success')
        return redirect(url_for('main.account'))

    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email

    context['image_file'] = url_for('static', filename='main/profile_pics/'+current_user.image_file)
    return render_template(template, **context)


@bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    template = 'main/create_post.html'
    form = PostForm()
    context = {
        'form': form,
        'title': 'New Post',
        'legend': 'New Post',
    }

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
        )
        post.save()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template(template, **context)


@bp.route('/post/<int:post_id>')
def post(post_id):
    template = 'main/post.html'
    post = Post.query.get_or_404(post_id)
    context = {
        'title': post.title,
        'post': post,
    }
    return render_template(template, **context)


@bp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    template = 'main/create_post.html'
    form = PostForm()
    context = {
        'title': 'Update Post',
        'legend': 'Update Post',
        'form': form,
    }

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.save()
        flash('Your post has been update!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template(template, **context)


@bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    post.delete()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@bp.route('/post/user/<string:user>', methods=['GET'])
def post_by_user(user):
    pass
