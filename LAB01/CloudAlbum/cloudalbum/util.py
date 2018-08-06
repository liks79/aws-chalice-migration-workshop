"""
    cloudalbum.util.py
    ~~~~~~~~~~~~~~~~~~~~~~~
    CloudAlbum is a sample application for TechSummit 2018 workshop.

    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime
from tzlocal import get_localzone
from cloudalbum.config import conf
from PIL import Image
import collections
import time
import os
import sys


def allowed_file_ext(filename):
    """
    Check the file extensions whether allowed file or not
    :param filename: file input (photo file)
    :return: True or False
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in conf['ALLOWED_EXTENSIONS']


def email_normalize(email):
    """
    Email normalization to get unique path.
    :param email: user email address.
    :return: normalized string value
    """
    return email.replace('@', '_at_').replace('.', '_dot_')


def save(upload_file, filename, email, app):
    """
    Upload input file (photo) to specific path for individual user.
    Save original file and thumbnail file.
    :param upload_file: file object
    :param filename: secure filename for upload
    :param email: user email address
    :param app: Flask.app
    :return: file size (byte)
    """
    path = os.path.join(conf['UPLOAD_FOLDER'], email_normalize(email))

    try:
        if not os.path.exists(path):
            os.makedirs(path)
            app.logger.info("Create folder: %s", path)

        original_full_path = os.path.join(path, filename)
        upload_file.save(original_full_path)
        file_size = os.stat(original_full_path).st_size
        make_thumbnails(path, filename, app)

    except Exception as e:
        app.logger.error('Error occurred while saving file:%s', e)
        raise e

    return file_size


def delete(app, filename, current_user):
    """
    Delete specific file (with thumbnail)
    :param app: Flask.app
    :param photo: specific photo ORM object
    :param current_user: Flask_login.current_user
    :return: None
    """
    try:
        path = os.path.join(conf['UPLOAD_FOLDER'], email_normalize(current_user.email))
        thumbnail = os.path.join(os.path.join(path, "thumbnail"), filename)
        original = os.path.join(path, filename)
        if os.path.exists(thumbnail):
            os.remove(thumbnail)
        if os.path.exists(original):
            os.remove(original)

    except Exception as e:
        app.logger.error('Error occurred while deleting file:%s', e)
        raise e


def make_thumbnails(path, filename, app):
    """
    Generate thumbnail from original image file.
    :param path: target path
    :param filename: secure file name
    :param app: Falsk.app
    :return: None
    """
    thumb_path = os.path.join(path, 'thumbnails')
    thumb_full_path = os.path.join(thumb_path, filename)

    app.logger.debug(thumb_path)
    app.logger.debug(thumb_full_path)

    try:
        if not os.path.exists(thumb_path):
            os.makedirs(thumb_path)
            app.logger.info("Create folder for thumbnails: %s", path)

        im = Image.open(os.path.join(path, filename))
        im = im.convert('RGB')
        im.thumbnail((conf['THUMBNAIL_WIDTH'], conf['THUMBNAIL_HEIGHT'], Image.ANTIALIAS))
        im.save(thumb_full_path)

    except Exception as e:
        app.logger.error("Thumbnails creation error : %s, %s", thumb_full_path, e)
        raise e


def sizeof_fmt(num):
    """
    Return human readable file size
    :param num: file size (byte)
    :return: human readable file size string.
    """
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def check_variables():
    """
    Check the key variables for application running
    :return: if verification failed, exit with -1
    """
    if (conf['DB_URL'] is None) or (conf['GMAPS_KEY'] is None):
        print('DB_URL or GMAPS_KEY are not configured!', file=sys.stderr)
        print('Check your environment variables!', file=sys.stderr)
        exit(-1)


def log_path_check(log_path):
    """

    :param log_path:
    :return: None
    """
    try:
        if not os.path.exists(log_path):
            os.makedirs(log_path)
    except Exception as e:
        raise e


current_milli_time = lambda: int(round(time.time() * 1000))


def the_time_now():
    # utc_tz = pytz.timezone('UTC')
    local_tz = get_localzone()
    return datetime.now(local_tz)



