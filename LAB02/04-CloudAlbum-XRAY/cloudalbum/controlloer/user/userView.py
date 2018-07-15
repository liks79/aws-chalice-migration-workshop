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
from flask import current_app as app, session
from cloudalbum.controlloer.errors import errorHandler
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from flask import jsonify
from cloudalbum.model.models_ddb import UserModel
from cloudalbum.config import options
import uuid
import boto3

blueprint = Blueprint('userView', __name__)


# @blueprint.route('/')
# @blueprint.route('/signin', methods=['GET', 'POST'])
# def signin():
#     """
#     Sign-in processing module
#     :return: if success render site home HTML page, or render sign-in HTML page again.
#     """
#
#     form = LoginForm(request.form)
#
#     if request.method == 'POST' and form.validate():
#         app.logger.debug(form.data)
#         try:
#             user = None
#             for item in UserModel.email_index.query(form.email.data):
#                 user = item
#
#             password_matched = check_password_hash(user.password, form.password.data)
#             app.logger.debug(user)
#
#             if user and password_matched:
#                 app.logger.info('Login success')
#                 login_user(user)
#                 return redirect(url_for('siteView.home'))
#             else:
#                 flash('Invalid email or password. Please try again!')
#                 app.logger.debug('Is hashed password matched?: %s - %s : %s ',
#                                  password_matched,
#                                  user.password,
#                                  generate_password_hash(form.password.data))
#                 return redirect(url_for('userView.signin'))
#
#         except Exception as e:
#             app.logger.error(e)
#             flash('Invalid email or password. Please try again!')
#             return redirect(url_for('userView.signin'))
#
#     return render_template('signin.html')


@blueprint.route('/')
@blueprint.route('/signin')
def signin():
    """Login route"""
    # http://docs.aws.amazon.com/cognito/latest/developerguide/login-endpoint.html
    session['csrf_state'] = uuid.uuid4().hex
    cognito_login = ("https://%s/"
                     "login?response_type=code&client_id=%s"
                     "&state=%s"
                     "&redirect_uri=%s/callback" %
                     (options['COGNITO_DOMAIN'], options['COGNITO_CLIENT_ID'], session['csrf_state'],
                      options['BASE_URL']))

    app.logger.debug(cognito_login)

    return redirect(cognito_login)


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
            user_exist = None
            for item in UserModel.email_index.query(form.email.data):
                user_exist = item.email

            if not user_exist:
                user = UserModel(uuid.uuid4().hex)
                user.email = form.email.data
                user.password = generate_password_hash(form.password.data)
                user.username = form.username.data
                user.save()
                app.logger.debug(user)
                flash('You have been signed up successfully!')
                return redirect(url_for('userView.signin', form=form))

            else:
                flash('Your email is already registered. Please try again!')
                app.logger.debug('Email is already registered : %s ', form.email.data)
                return redirect(url_for('userView.signup', form=form))

        except Exception as e:
            app.logger.error(e)
            return errorHandler.server_error(e)

    return render_template('signup.html')


# @blueprint.route('/<user_id>/edit', methods=['GET'])
# @blueprint.route('/<user_id>', methods=['PUT'])
# @login_required
# def edit(user_id):
#     """
#     Edit user profile and save.
#     :param user_id: target user id
#     :return: Render signup template or return Json data
#     """
#
#     if request.method == 'GET':
#         try:
#             user = UserModel.get(user_id)
#             app.logger.debug(user)
#         except Exception as e:
#             app.logger.error(e)
#             flash("DB operation failed! Try again.")
#
#     if request.method == 'PUT':
#         try:
#             user = UserModel.get(user_id)
#             data = request.get_json()
#             app.logger.debug(data)
#             user.update(actions=[
#                 UserModel.username.set(data['username']),
#                 UserModel.password.set(generate_password_hash(data['password']))
#             ])
#             return jsonify(update='success')
#
#         except Exception as e:
#             app.logger.error(e)
#             return jsonify(update='failed')
#
#     return render_template('signup.html', user=user)



@blueprint.route('/<user_id>/edit', methods=['GET'])
@blueprint.route('/<user_id>', methods=['PUT'])
@login_required
def edit(user_id):
    """
    Edit user profile and save.
    :param user_id: target user id
    :return: Render signup template or return Json data
    """

    if request.method == 'GET':
        try:
            user = UserModel()
            user.id = current_user.id
            user.email = current_user.email
            user.username = current_user.username

            app.logger.debug(user)
        except Exception as e:
            app.logger.error(e)
            flash("DB operation failed! Try again.")

    if request.method == 'PUT':
        try:
            data = request.get_json()

            app.logger.debug(data)

            client = boto3.client('cognito-idp')

            response = client.admin_update_user_attributes(
                UserPoolId=options['COGNITO_POOL_ID'],
                Username=current_user.id,
                UserAttributes=[
                    {
                        'name': data['username'],
                        'password': data['password']
                    },
                ]
            )
            app.logger.debug(response)

            return jsonify(update='success')

        except Exception as e:
            app.logger.error(e)
            return jsonify(update='failed')

    return render_template('signup.html', user=user)

# @blueprint.route('/signout', methods=['GET'])
# @login_required
# def signout():
#     """
#     Sign-out specific user
#     :return: render sign-in template
#     """
#     app.logger.debug('Sign-out : %s', current_user.username)
#     flash('You have been signed out successfully.')
#     logout_user()
#     return redirect(url_for('userView.signin'))


@blueprint.route('/signout')
@login_required
def signout():
    """Logout route"""
    # http://docs.aws.amazon.com/cognito/latest/developerguide/logout-endpoint.html
    logout_user()
    cognito_logout = ("https://%s/"
                      "logout?response_type=code&client_id=%s"
                      "&logout_uri=%s/" 
                      "&redirect_uri=%s/" %
                      (options['COGNITO_DOMAIN'], options['COGNITO_CLIENT_ID'], options['BASE_URL'], options['BASE_URL']))
    return redirect(cognito_logout)


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

