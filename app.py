from flask import Flask, request, render_template, redirect, flash
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,  check_password_hash
from datetime import datetime
import pandas as pd
import random
from forms import LoginForm
import db_controller

user_db = db_controller.Students()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vr_cell'

login_manager = LoginManager(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)

@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


db.create_all()
db.session.commit()

u1 = User(username='mmvvrr1', email='mmvvrr1@gmail.com')
u1.set_password("admin1")

u2 = User(username='admin2', email='same@gmail.com')
u2.set_password("admin2")

db.session.add_all([u1, u2])
db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@app.route('/')
def index():  # put application's code here
    return render_template('Главная.html')

@app.route('/download')
def download():  # put application's code here
    return render_template('Загрузить.html')

@app.route('/login')
def login():  # put application's code here
    return render_template('Войти.html')

@app.route('/api/', methods=['GET', 'POST'])
def api():  # put application's code here
    data = request.get_json()
    password = user_db.get_pass(data['_field_login'])
    if password == 0:
        print('Пользователя не существует')
    else:
        if password == data['_field_password']:
            print('Успешно')
        else:
            print('Неверный пароль')
    print(data)
    return 'Success'


if __name__ == '__main__':
    app.run()
