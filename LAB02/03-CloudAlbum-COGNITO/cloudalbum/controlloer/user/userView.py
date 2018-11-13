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
from cloudalbum.model.models_ddb import User
from cloudalbum.config import conf
import uuid
import boto3

blueprint = Blueprint('userView', __name__)


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
                     (conf['COGNITO_DOMAIN'], conf['COGNITO_CLIENT_ID'], session['csrf_state'],
                      conf['BASE_URL']))

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
            for item in User.email_index.query(form.email.data):
                user_exist = item.email

            if not user_exist:
                user = User(uuid.uuid4().hex)
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


@blueprint.route('/<user_id>/edit', methods=['GET', 'PUT'])
@login_required
def edit(user_id):
    """
    Edit user profile and save.
    :param user_id: target user id
    :return: Render signup template or return Json data
    """
    password_reset = "https://" \
                     "{0}/forgotPassword?response_type=code&client_id=" \
                     "{1}&redirect_uri=" \
                     "{2}"\
        .format(conf['COGNITO_DOMAIN'],
                conf['COGNITO_CLIENT_ID'],
                conf['BASE_URL']+'/callback')

    if request.method == 'GET':
        try:
            user = User()
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

            client = boto3.client('cognito-idp')
            response = client.admin_update_user_attributes(
                UserPoolId=conf['COGNITO_POOL_ID'],
                Username=current_user.id,
                UserAttributes=[
                    {
                        'Name': 'name',
                        'Value': data['username']
                    },
                ]
            )

            app.logger.debug(response)
            session['name'] = data['username']

            return jsonify(update='success')

        except Exception as e:
            app.logger.error(e)
            return jsonify(update='failed')

    return render_template('signup.html', user=user, password_reset=password_reset)


@blueprint.route('/signout')
@login_required
def signout():
    """Logout route"""
    # http://docs.aws.amazon.com/cognito/latest/developerguide/logout-endpoint.html
    logout_user()
    cognito_logout = ("https://%s/"
                      "logout?response_type=code&client_id=%s"
                      "&logout_uri=%s" 
                      "&redirect_uri=%s" %
                      (conf['COGNITO_DOMAIN'], conf['COGNITO_CLIENT_ID'], conf['BASE_URL'], conf['BASE_URL']))
    return redirect(cognito_logout)


