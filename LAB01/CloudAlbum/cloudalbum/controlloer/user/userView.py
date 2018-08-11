"""
    controller.user.userView.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CloudAlbum is a sample application for TechSummit 2018 workshop.

    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import current_app as app
from cloudalbum.controlloer.errors import errorHandler
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from cloudalbum.model.models import db
from cloudalbum.model.models import User
from flask import jsonify

blueprint = Blueprint('userView', __name__)


@blueprint.route('/')
@blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    Sign-in processing module
    :return: if success render site home HTML page, or render sign-in HTML page again.
    """

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        app.logger.debug(form.data)
        try:
            user = db.session.query(User).filter_by(email=form.email.data).first()
            password_matched = check_password_hash(user.password, form.password.data)
            app.logger.debug(user)

            if user and password_matched:
                app.logger.info('Login success')
                login_user(user)
                return redirect(url_for('siteView.home'))
            else:
                flash('Invalid email or password. Please try again!')
                app.logger.debug('Is hashed password matched?: %s - %s : %s ',
                                 password_matched,
                                 user.password,
                                 generate_password_hash(form.password.data))
                return redirect(url_for('userView.signin'))

        except Exception as e:
            app.logger.error(e)
            flash('Invalid email or password. Please try again!')
            return redirect(url_for('userView.signin'))

    return render_template('signin.html')


# @blueprint.route('/new', methods=['GET', 'POST'])
# def signup():
#     """
#     Sign-up view function.
#     :return: if success, render sign-in HTML page.
#     """
#
#     form = UserForm(request.form)
#
#     if request.method == 'POST' and form.validate():
#         app.logger.debug(form.data)
#
#         try:
#             user_exist = db.session.query(User).filter_by(email=form.email.data).first()
#             if not user_exist:
#                 user = User(form.username.data, form.email.data, generate_password_hash(form.password.data))
#                 app.logger.debug(user)
#                 db.session.add(user)
#                 db.session.commit()
#                 flash('You have been signed up successfully!')
#                 return redirect(url_for('userView.signin', form=form))
#             else:
#                 flash('Your email is already registered. Please try again!')
#                 app.logger.debug('Email is already registered : %s ', form.email.data)
#                 return redirect(url_for('userView.signup', form=form))
#
#         except Exception as e:
#             app.logger.error(e)
#             db.session.rollback()
#             return errorHandler.server_error(e)
#
#     return render_template('signup.html')


@blueprint.route('/new', methods=['GET', 'POST'])
def signup():
    """
    Sign-up view function.
    :return: if success, render sign-in HTML page.
    """

    form = UserForm(request.form)

    if request.method == 'POST' and form.validate():
        app.logger.debug(form.data)

        try:
            user_exist = db.session.query(User).filter_by(email=form.email.data).first()
            if not user_exist:
                user = User(form.username.data, form.email.data, generate_password_hash(form.password.data))
                app.logger.debug(user)
                db.session.add(user)
                db.session.commit()
                flash('You have been signed up successfully!')
                return redirect(url_for('userView.signin', form=form))
            else:
                flash('Your email is already registered. Please try again!')
                app.logger.debug('Email is already registered : %s ', form.email.data)
                return redirect(url_for('userView.signup', form=form))

        except Exception as e:
            app.logger.error(e)
            db.session.rollback()
            return errorHandler.server_error(e)

    return render_template('signup.html')


@blueprint.route('/<user_id>/edit', methods=['GET', 'PUT'])
@login_required
def edit(user_id):
    """
    Edit user profile and save.
    :param user_id: target user id
    :return: Render signup template or return Json data
    """

    if request.method == 'GET':
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            app.logger.debug(user)
        except Exception as e:
            app.logger.error(e)
            flash("DB operation failed! Try again.")

    if request.method == 'PUT':
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            data = request.get_json()
            app.logger.debug(data)
            user.username = data['username']
            user.password = generate_password_hash(data['password'])
            db.session.merge(user)
            db.session.commit()
            return jsonify(update='success')

        except Exception as e:
            app.logger.error(e)
            return jsonify(update='failed')

    return render_template('signup.html', user=user)


@blueprint.route('/signout', methods=['GET'])
@login_required
def signout():
    """
    Sign-out specific user
    :return: render sign-in template
    """
    app.logger.debug('Sign-out : %s', current_user.username)
    flash('You have been signed out successfully.')
    logout_user()
    return redirect(url_for('userView.signin'))


class LoginForm(FlaskForm):
    """
    LoginForm class for processing login form data
    """
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class UserForm(FlaskForm):
    """
    UserForm class for processing user register from form data
    """
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    password_confirm = StringField('password_confirm', validators=[DataRequired()])

