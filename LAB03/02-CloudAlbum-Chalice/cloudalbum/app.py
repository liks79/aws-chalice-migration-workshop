from chalice import Response
from chalice import Chalice, AuthResponse
from chalicelib import util
from chalicelib.config import conf, S3_STATIC_URL, cors_config
from chalicelib.util import verify, get_user
from chalicelib.models_ddb import User, Photo
from requests.auth import HTTPBasicAuth
from urllib.parse import parse_qs
from datetime import datetime, timedelta
from jinja2 import Environment, PackageLoader, select_autoescape
import requests
import uuid
import logging
import tempfile
import io
import boto3


app = Chalice(app_name='cloudalbum')
app.debug = True
app.log.setLevel(logging.DEBUG)

env = Environment(
    loader=PackageLoader(__name__, 'chalicelib/templates'),
    autoescape=select_autoescape(['html', 'xml']))


@app.route('/home', methods=['GET'], cors=cors_config)
def home():
    t = env.get_template('home.html')
    user = get_user(app, User())

    result = Photo.query(user.id)
    body = t.render(current_user=user, photos=result, presigned_url=util.presigned_url,
                    s3_static_url=S3_STATIC_URL)

    return Response(body=body, status_code=200, headers={
        "Content-Type": "text/html"})


@app.route('/users/{user_id}/edit', methods=['GET'], cors=cors_config)
def user_edit_form(user_id):
    t = env.get_template('signup.html')
    user = get_user(app, User())

    body = t.render(user=user, password_reset=util.get_password_reset_url(),
                    s3_static_url=S3_STATIC_URL)

    return Response(body=body, status_code=200, headers={
        "Content-Type": "text/html"})



@app.route('/users/{user_id}/edit', methods=['PUT'], cors=cors_config,
           content_types=['application/x-www-form-urlencoded', 'charset=utf-8'])
def user_edit(user_id):
    t = env.get_template('home.html')
    user = get_user(app, User())

    parsed = parse_qs(app.current_request.raw_body.decode())
    username = parsed.get('username')[0]

    try:
        client = boto3.client('cognito-idp')
        response = client.admin_update_user_attributes(
            UserPoolId=conf['COGNITO_POOL_ID'],
            Username=user.id,
            UserAttributes=[
                {
                    'Name' : 'name',
                    'Value': username
                },
            ]
        )
    except Exception as e:
        return Response(body={'update': 'failed'}, status_code=200, headers={"Content-Type": "application/json"})

    return Response(body={'update': 'success'}, status_code=200, headers={"Content-Type": "application/json"})


@app.route('/photos/map', methods=['GET'], cors=cors_config)
def map_view():
    t = env.get_template('map.html')
    user = get_user(app, User())

    photo_list = Photo.query(user.id)
    body = t.render(current_user=user, photos=photo_list, gmaps_key=conf['GMAPS_KEY'],
                    presigned_url=util.presigned_url, s3_static_url=S3_STATIC_URL)

    return Response(body=body, status_code=200, headers={
        "Content-Type": "text/html"})


@app.route('/photos/{photo_id}/map', methods=['GET'], cors=cors_config)
def map_view_specific(photo_id):
    t = env.get_template('map.html')
    user = get_user(app, User())

    photo = Photo.get(user.id, photo_id)
    photo_list = list()
    photo_list.append(photo)

    body = t.render(current_user=user, photos=photo_list, gmaps_key=conf['GMAPS_KEY'],
                    presigned_url=util.presigned_url, s3_static_url=S3_STATIC_URL)

    return Response(body=body, status_code=200, headers={
        "Content-Type": "text/html"})


@app.route('/photos/new', methods=['GET'], cors=cors_config)
def upload_form():
    user = get_user(app, User())
    t = env.get_template('upload.html')
    body = t.render(current_user=user, gmaps_key=conf['GMAPS_KEY'], s3_static_url=S3_STATIC_URL)
    response = Response(body=body, status_code=200,
                        headers={"Content-Type": "text/html"})
    return response


@app.route('/photos/new', methods=['POST'], content_types=['multipart/form-data'], cors=cors_config)
def upload():
    # flash('Your file upload have been completed successfully!')

    user = get_user(app, User())
    form = util.get_parts(app)

    filename_orig = form['filename_origin'][0].decode('utf-8')
    ext = (filename_orig.rsplit('.', 1)[1]).lower()
    filename = "{0}{1}.{2}".format(next(tempfile._get_candidate_names()), uuid.uuid4().hex, ext)

    stream = io.BytesIO(form['photo'][0])
    size = util.save_s3_chalice(stream, filename, user.email, app)

    taken_date = datetime.strptime(form['taken_date'][0].decode('utf-8'), "%Y:%m:%d %H:%M:%S")
    photo = Photo(user.id, util.current_milli_time())
    photo.tags = form['tags'][0].decode('utf-8')
    photo.desc = form['desc'][0].decode('utf-8')
    photo.filename_orig = 'test'
    photo.filename = filename
    photo.filesize = size
    photo.geotag_lat = form['lat'][0].decode('utf-8')
    photo.geotag_lng = form['lng'][0].decode('utf-8')
    photo.upload_date = util.the_time_now()
    photo.taken_date = taken_date
    photo.make = form['make'][0].decode('utf-8')
    photo.model = form['model'][0].decode('utf-8')
    photo.width = form['width'][0].decode('utf-8')
    photo.height = form['height'][0].decode('utf-8')
    photo.city = form['city'][0].decode('utf-8')
    photo.nation = form['nation'][0].decode('utf-8')
    photo.address = form['address'][0].decode('utf-8')
    photo.save()

    return Response(
        status_code=301,
        headers={'Location': '/api/home'},
        body=''
    )


@app.route('/photos/{photo_id}', methods=['DELETE'],
           content_types=['application/x-www-form-urlencoded', 'charset=utf-8'])
def photo_delete(photo_id):
    """
    Delete specific file (with thumbnail) and delete DB record.
    :param photo_id: target photo id
    :return: Json data remove:fail or success
    """
    user = get_user(app, User())

    app.log.debug("Photo delete request: %s", photo_id)
    try:
        photo = Photo.get(user.id, int(photo_id))
        photo.delete()

        util.delete_s3(app, photo.filename, user)

        # flash('Successfully removed!')
        app.log.debug('Successfully removed!')

    except Exception as e:
        app.log.error(e)
        # flash('Error occurred! Please try again.')
        return Response(body={'remove': 'fail'}, status_code=200, headers={"Content-Type": "application/json"})

    return Response(body={'remove': 'success'}, status_code=200, headers={"Content-Type": "application/json"})


@app.route('/', methods=['GET'])
def signin():
    """Login route"""
    # http://docs.aws.amazon.com/cognito/latest/developerguide/login-endpoint.html

    cognito_login = "https://{0}/"\
                    "login?response_type=code&client_id={1}"\
                    "&state={2}"\
                    "&redirect_uri={3}/callback".format(
                        conf['COGNITO_DOMAIN'],
                        conf['COGNITO_CLIENT_ID'],
                        uuid.uuid4().hex,
                        conf['BASE_URL'])

    app.log.debug(cognito_login)

    return Response(
        status_code=301,
        headers={'Location': cognito_login},
        body=''
    )

@app.route('/users/signout', methods=['GET'])
def signout():
    """Login route"""
    # http://docs.aws.amazon.com/cognito/latest/developerguide/login-endpoint.html

    cognito_logout = ("https://{0}/"\
                      "logout?response_type=code&client_id={1}"\
                      "&logout_uri={2}"\
                      "&redirect_uri={3}".format(
                      conf['COGNITO_DOMAIN'],
                      conf['COGNITO_CLIENT_ID'],
                      conf['BASE_URL'], conf['BASE_URL']))

    app.log.debug(cognito_logout)

    return Response(
        status_code=301,
        headers={'Location': cognito_logout},
        body=''
    )


@app.route('/photos/search', methods=['POST'], content_types=['application/x-www-form-urlencoded', 'charset=utf-8'])
def search():
    """
    Search function for description and tags in Photo table.
    :return: List of photo object which retrieved DB.
    """
    t = env.get_template('home.html')
    user = get_user(app, User())

    parsed = parse_qs(app.current_request.raw_body.decode())
    keyword = parsed.get('search')[0]

    photo_pages = Photo.query(user.id, Photo.tags.contains(keyword) | Photo.desc.contains(keyword))

    body = t.render(current_user=user, photos=photo_pages, presigned_url=util.presigned_url,
                    msg="Search results for '{0}'.. ".format(keyword), s3_static_url=S3_STATIC_URL)

    return Response(body=body, status_code=200, headers={
        "Content-Type": "text/html"})


@app.route('/callback')
def callback():
    """Exchange the 'code' for Cognito tokens"""
    #http://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
    csrf_state = app.current_request.query_params.get('state')
    code = app.current_request.query_params.get('code')
    request_parameters = {'grant_type': 'authorization_code',
                          'client_id': conf['COGNITO_CLIENT_ID'],
                          'code': code,
                          "redirect_uri": conf['BASE_URL'] + "/callback"}

    response = requests.post("https://{0}/oauth2/token".format(conf['COGNITO_DOMAIN']),
                             data=request_parameters,
                             auth=HTTPBasicAuth(conf['COGNITO_CLIENT_ID'],
                                                conf['COGNITO_CLIENT_SECRET']))

    # the response:
    # http://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html
    # if response.status_code == requests.codes.ok and csrf_state == session['csrf_state']:
    if response.status_code == requests.codes.ok:
        verify(response.json()["access_token"])
        id_token = verify(response.json()["id_token"], response.json()["access_token"])

        app.log.debug(response.json()["access_token"])
        app.log.debug(id_token)

        access_token=response.json()["access_token"]

        # expires = datetime.utcnow() + timedelta(hours=1)

        return Response(
            status_code=301,
            headers= {
                'Authorization': access_token,
                # 'Set-Cookie': 'token={0}; expires={1}'.format(access_token, expires),
                'Set-Cookie': 'sid={0}; token={1}'.format(id_token["cognito:username"], access_token),
                'location': '/api/home'
            },
            body=''
        )

    else:
        return Response(
            status_code=301,
            headers={'Location': '/api'},
            body=''
        )

# https://chalice.readthedocs.io/en/latest/api.html
#
# @app.on_s3_event('mybucket', events=['s3:ObjectCreated:Put'],
#                  prefix='images/', suffix='.jpg')
# def resize_image(event):
#     with tempfile.NamedTemporaryFile('w') as f:
#         s3.download_file(event.bucket, event.key, f.name)
#         resize_image(f.name)
#         s3.upload_file(event.bucket, 'resized/%s' % event.key, f.name)


