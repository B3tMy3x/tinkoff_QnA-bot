import os
from datetime import timedelta

from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename

from app import app, db, allowed_file
from app.forms import RegistrationForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.config import Config

import time


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        else:
            flash('Email address already exists. Please use a different email address.')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(weeks=1))
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('message')
        if user_message == 'Привет!':
            response = 'Вас приветствует Q&A-бот Тинькофф!'
        elif user_message == 'Может ли банк увеличить процентную ставку по кредиту наличными?':
            response = 'Нет, банк не может в одностороннем порядке повысить ставки.'
        else:
            response = 'Извините, я не могу ответить на этот вопрос'
        return jsonify({"response": response})

    return render_template('chat.html')



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS