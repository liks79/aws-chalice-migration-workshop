"""
    controller.photo.photoView.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CloudAlbum is a sample application for TechSummit 2018 workshop.

    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import current_app as app, make_response
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, HiddenField, TextAreaField, validators
from wtforms.validators import DataRequired
from cloudalbum.controlloer.errors import errorHandler
from datetime import datetime
from werkzeug.utils import secure_filename
from cloudalbum import util
from math import ceil
from flask import jsonify
from cloudalbum.config import conf
from cloudalbum.model.models_ddb import Photo
import uuid
import os


blueprint = Blueprint('photoView', __name__)


@blueprint.route('/', methods=['GET'])
@login_required
def photos():
    """
    Retrieve uploaded photo information
    :param page: page number for the pagination.
    :return: HTML template for photo list
    """

    results = Photo.query(current_user.id)

    return render_template('home.html', photos=results, gmaps_key=conf['GMAPS_KEY'],
                           sizeof_fmt=util.sizeof_fmt, current_user=current_user)


@blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def upload():
    """
    Photo file upload  function
    :return: HTML template for upload form or uploaded photo list
    """

    form = PhotoForm(request.form)

    if request.method == 'POST':
        app.logger.debug(form.data)
        app.logger.debug("form.taken_date.data:%s", form.taken_date.data)
        upload_photo = request.files['photo']
        ext = (upload_photo.filename.rsplit('.', 1)[1]).lower()
        filename = secure_filename("{0}.{1}".format(uuid.uuid4(), ext))
        taken_date = datetime.strptime(form.taken_date.data, "%Y:%m:%d %H:%M:%S")

        app.logger.debug("take_date:{0}".format(taken_date))

        try:
            app.logger.debug(current_user)
            size = util.save(upload_photo, filename, current_user.email, app)

            photo = Photo(current_user.id, util.current_milli_time())
            photo.tags = form.tags.data
            photo.desc = form.desc.data
            photo.filename_orig = upload_photo.filename
            photo.filename = filename
            photo.filesize = size
            photo.geotag_lat = form.lat.data
            photo.geotag_lng = form.lng.data
            photo.upload_date = util.the_time_now()
            photo.taken_date = taken_date
            photo.make = form.make.data
            photo.model = form.model.data
            photo.width = form.width.data
            photo.height = form.height.data
            photo.city = form.city.data
            photo.nation = form.nation.data
            photo.address = form.address.data
            photo.save()

            flash('Your file upload have been completed successfully!')
            return redirect(url_for("photoView.photos", form=form, gmaps_key=conf['GMAPS_KEY']))

        except Exception as e:
            app.logger.error(e)
            util.delete(app, filename, current_user)
            return errorHandler.server_error(e)

    return render_template('upload.html', form=form, gmaps_key=conf['GMAPS_KEY'])


@blueprint.route('/<int:photo_id>', methods=['DELETE'])
@login_required
def photo_delete(photo_id):
    """
    Delete specific file (with thumbnail) and delete DB record.
    :param photo_id: target photo id
    :return: Json data remove:fail or success
    """

    app.logger.debug("Photo delete request: %s", photo_id)
    try:
        ## TODO #4 : Review following code to delete uploaded photo information in DynamoDB.
        ## -- begin --
        photo = Photo.get(current_user.id, photo_id)
        photo.delete()
        ## -- end --

        util.delete(app, photo.filename, current_user)
        flash('Successfully removed!')
        app.logger.debug('Successfully removed!')

    except Exception as e:
        app.logger.error(e)
        flash('Error occurred! Please try again.')
        return jsonify(remove='fail')

    return jsonify(remove='success')


@blueprint.route('/<int:photo_id>', methods=['GET'])
@login_required
def photo_url(photo_id):
    """
    Return image url for thumbnail and original photo.
    :param photo_id: target photo id
    :return: image url for authenticated user
    """
    mode = request.args.get('mode')
    try:
        photo = Photo.get(current_user.id, photo_id)
        path = os.path.join(conf['UPLOAD_FOLDER'], util.email_normalize(current_user.email))

        if mode == "thumbnail":
            full_path = os.path.join(os.path.join(path, "thumbnails"), photo.filename)
        else:
            full_path = os.path.join(path, photo.filename)

        with open(full_path, 'rb') as f:
            contents = f.read()
            resp = make_response(contents)

    except Exception as e:
        app.logger.error(e)
        flash('Error occurred! Please try again.')
        return 'http://placehold.it/400x300'

    app.logger.debug("mode: %s, %s", mode, full_path)
    resp.content_type = "image/jpeg"
    return resp


@blueprint.route('/<photo_id>/edit', methods=['GET'])
@blueprint.route('/<photo_id>', methods=['PUT'])
@login_required
def edit(photo_id):
    """
    Edit uploaded photo information.
    :param photo_id: target photo id
    :return: HTML template for edit form or Json data
    """

    if request.method == 'GET':
        photo = Photo.get(current_user.id, photo_id)
        return render_template('upload.html', photo=photo, gmaps_key=conf['GMAPS_KEY'])

    elif request.method == 'PUT':
        data = request.get_json()
        try:
            photo = Photo.get(current_user.id, photo_id)
            photo.tags = data['tags']
            photo.desc = data['desc']
            photo.geotag_lat = data['lat']
            photo.geotag_lng = data['lng']
            photo.city = data['city']
            photo.nation = data['nation']
            photo.address = data['address']
            photo.save()
            return jsonify(update='success')

        except Exception as e:
            app.logger.error(e)
            return jsonify(update='fail')
    else:
        return redirect(url_for("/", gmaps_key=conf['GMAPS_KEY']))


@blueprint.route('/search', methods=['POST'])
@login_required
def search():
    """
    Search function for description and tags in Photo table.
    :return: List of photo object which retrieved DB.
    """

    ## TODO #3 : Review following code to search result via keyword in the DynamoDB.
    ## -- begin --
    keyword = request.form['search']
    photo_pages = Photo.query(current_user.id,
                              Photo.tags.contains(keyword) |
                              Photo.desc.contains(keyword))
    ## -- end --

    flash("Search results for '{0}'.. ".format(keyword))
    return render_template('home.html', photos=photo_pages, gmaps_key=conf['GMAPS_KEY'])




@blueprint.route('/map', methods=['GET'])
@blueprint.route('/<int:photo_id>/map', methods=['GET'])
@login_required
def map_view(photo_id=None):
    """
    Map view with photo marker.
    :param photo_id: target photo id
    :return: HTML template for the map.
    """

    if not photo_id:
        photo_list = Photo.query(current_user.id)
        app.logger.debug("photo_id: {0}".format(photo_id))
    else:
        photo = Photo.get(current_user.id, photo_id)
        photo_list = list()
        photo_list.append(photo)


    return render_template("map.html", photos=photo_list, gmaps_key=conf['GMAPS_KEY'])


class PhotoForm(FlaskForm):
    """
    Form class to process form input data
    """
    photo = FileField('photo')
    tags = StringField('tags', [validators.Length(min=1, max=400, message='Please enter no more than 400 characters.')])
    desc = TextAreaField('desc', [validators.Length(min=1, max=400, message='Please enter no more than 400 characters.')])
    # EXIF DATA
    lat = HiddenField('lat', [DataRequired(message='Latitude information is missing!')])
    lng = HiddenField('lng', [DataRequired(message='Longitude information is missing!')])
    taken_date = HiddenField('Taken Date')
    make = HiddenField('make')
    model = HiddenField('model')
    width = HiddenField('width')
    height = HiddenField('height')
    city = HiddenField('city')
    nation = HiddenField('nation')
    address = HiddenField('address')
    formatted_address = HiddenField('formatted_address')

