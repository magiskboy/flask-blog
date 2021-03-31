import sqlalchemy as sa
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


class SQLAlchemy(BaseSQLAlchemy):
    def init_app(self, app):
        super().init_app(app)
        Migrate(app, self)


db = SQLAlchemy()


class BaseModel:
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.TIMESTAMP(), default=sa.func.now())
    updated_at = sa.Column(sa.TIMESTAMP(), onupdate=sa.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(BaseModel, UserMixin, db.Model):
    __tablename__ = "users"

    name = sa.Column(sa.String(100), nullable=False)
    email = sa.Column(sa.String(400), unique=True, nullable=False)
    image_file = sa.Column(
        sa.String(500), nullable=False, default="default.jpg"
    )
    hash_password = sa.Column(sa.String(128), nullable=False)
    verify_on_google = sa.Column(sa.Boolean(), default=False)
    verify_on_facebook = sa.Column(sa.Boolean(), default=False)

    @property
    def password(self):
        raise AttributeError("This is an only-read attribute")

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)

    def __repr__(self):
        return f"<User {self.id}: {self.email}>"

    def __str__(self):
        return self.email


class Post(BaseModel, db.Model):
    __tablename__ = "posts"

    title = sa.Column(sa.String(50), nullable=False)
    content = sa.Column(sa.String(5000), nullable=False)
    author_id = sa.Column(
        sa.Integer(), sa.ForeignKey("users.id"), nullable=False
    )
    author = sa.orm.relationship(User, backref="posts")

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"

    def __str__(self):
        return self.title


class Comment(BaseModel, db.Model):
    __tablename__ = "comments"

    content = sa.Column(sa.String(200), nullable=False)
    post_id = sa.Column(
        sa.Integer(), sa.ForeignKey("posts.id"), nullable=False
    )
    user_id = sa.Column(
        sa.Integer(), sa.ForeignKey("users.id"), nullable=False
    )

    post = sa.orm.relationship(Post, backref="comments")
    user = sa.orm.relationship(User)
