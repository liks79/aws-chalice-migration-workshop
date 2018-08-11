"""
    controller.site.siteView.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CloudAlbum is a sample application for TechSummit 2018 workshop.

    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, redirect, url_for, session
from flask import current_app as app, jsonify, request, render_template_string
from flask_login import login_required, current_user, login_user
from jose import jwt
from requests.auth import HTTPBasicAuth
from cloudalbum import login
from cloudalbum.config import conf
from cloudalbum.model.models_ddb import User
from datetime import datetime
import requests
import import_string


blueprint = Blueprint('siteView', __name__)


## TODO #7: Review following code to retrieve JSON Web Key (JWK) from cognito
## https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html
## -- begin --
JWKS_URL = "https://cognito-idp.{0}.amazonaws.com/{1}/.well-known/jwks.json".\
    format(conf['AWS_REGION'], conf['COGNITO_POOL_ID'])
JWKS = requests.get(JWKS_URL).json()["keys"]
## -- end --


def verify(token, access_token=None):
    """Verify a cognito JWT"""
    # get the key id from the header, locate it in the cognito keys
    # and verify the key
    header = jwt.get_unverified_header(token)
    key = [k for k in JWKS if k["kid"] == header['kid']][0]
    id_token = jwt.decode(token, key, audience=conf['COGNITO_CLIENT_ID'], access_token=access_token)
    return id_token


@blueprint.route('home')
@blueprint.route('/')
@login_required
def home():
    """
    Home for authorized user
    :return: redirect photo list HTML template page
    """
    app.logger.debug(JWKS)
    app.logger.debug(current_user)
    return redirect(url_for('photoView.photos'))


@blueprint.route('/callback')
def callback():
    """Exchange the 'code' for Cognito tokens"""
    #http://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
    csrf_state = request.args.get('state')
    code = request.args.get('code')
    request_parameters = {'grant_type': 'authorization_code',
                          'client_id': conf['COGNITO_CLIENT_ID'],
                          'code': code,
                          "redirect_uri": conf['BASE_URL'] + "/callback"}

    response = requests.post("https://%s/oauth2/token" % conf['COGNITO_DOMAIN'],
                             data=request_parameters,
                             auth=HTTPBasicAuth(conf['COGNITO_CLIENT_ID'],
                                                conf['COGNITO_CLIENT_SECRET']))

    # the response:
    # http://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html
    if response.status_code == requests.codes.ok:
        verify(response.json()["access_token"])
        id_token = verify(response.json()["id_token"], response.json()["access_token"])

        app.logger.debug(id_token)

        ## TODO #8: Review following code to set up User objedct using id_token from Cognito
        ## -- begin --
        user = User()
        user.id = id_token["cognito:username"]
        user.email = id_token["email"]
        user.username = id_token["name"]

        session['id'] = id_token["cognito:username"]
        session['email'] = id_token["email"]
        session['name'] = id_token["name"]
        session['expires'] = id_token["exp"]
        session['refresh_token'] = response.json()["refresh_token"]

        login_user(user, remember=True)
        ## -- begin --

        return redirect(url_for("siteView.home"))

    else:
        return render_template_string("<h1>ERROR!</h1>")



@blueprint.route('routes', methods=['GET'])
def routes_info():
    """Print all defined routes and their endpoint docstrings

    This also handles flask-router, which uses a centralized scheme
    to deal with routes, instead of defining them as a decorator
    on the target function.
    """
    routes = []
    for rule in app.url_map.iter_rules():
        try:
            if rule.endpoint != 'static':
                if hasattr(app.view_functions[rule.endpoint], 'import_name'):
                    import_name = app.view_functions[rule.endpoint].import_name
                    obj = import_string(import_name)
                    routes.append({rule.rule: "%s\n%s" % (",".join(list(rule.methods)), obj.__doc__)})
                else:
                    routes.append({rule.rule: app.view_functions[rule.endpoint].__doc__})
        except Exception as exc:
            routes.append({rule.rule:
                           "(%s) INVALID ROUTE DEFINITION!!!" % rule.endpoint})
            route_info = "%s => %s" % (rule.rule, rule.endpoint)
            app.logger.error("Invalid route: %s" % route_info, exc_info=True)
            # func_list[rule.rule] = obj.__doc__

    return jsonify(code=200, data=routes)


@login.user_loader
def user_loader(session_token):
    """Populate user object, check expiry"""
    if "expires" not in session:
        return None

    app.logger.debug(session_token)
    app.logger.debug(session)

    user = User()
    user.id = session_token
    user.username = session['name']
    user.email = session['email']

    return user
