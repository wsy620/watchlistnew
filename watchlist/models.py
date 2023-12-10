# 2. 数据库结构
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from werkzeug.security import check_password_hash, generate_password_hash

from watchlist import db


class MovieInfo(db.Model):
    __tablename__ = 'movie_info'
    movie_id = db.Column(db.String(10), primary_key=True)
    movie_name = db.Column(db.String(20), nullable=False)
    release_date = db.Column(db.DateTime)
    country = db.Column(db.String(20))
    movie_type = db.Column('type', db.String(10))
    year = db.Column(db.Integer, CheckConstraint('year>=1000 and year<=2100'))

    def to_json(self):
        return {
            'movie_id': self.movie_id,
            'movie_name': self.movie_name,
            'release_date': str(self.release_date),
            'country': self.country,
            'type': self.movie_type,
            'year': self.year
        }


class MovieBox(db.Model):
    __tablename__ = 'movie_box'
    movie_id = db.Column(db.String(10), primary_key=True)
    box = db.Column(db.Float)

    def to_json(self):
        return {
            'movie_id': self.movie_id,
            'box': self.box
        }


class ActorInfo(db.Model):
    __tablename__ = 'actor_info'
    actor_id = db.Column(db.String(10), primary_key=True)
    actor_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(20))

    def to_json(self):
        return {
            'actor_id': self.actor_id,
            'actor_name': self.actor_name,
            'gender': self.gender,
            'act_country': self.country
        }


class MovieActorRelation(db.Model):
    __tablename__ = 'movie_actor_relation'
    id = db.Column(db.String(10), primary_key=True)
    movie_id = db.Column(db.String(10), db.ForeignKey('movie_info.movie_id'))
    actor_id = db.Column(db.String(10), db.ForeignKey('actor_info.actor_id'))
    relation_type = db.Column(db.String(20))

    def to_json(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
            'relation_type': self.relation_type
        }


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值
