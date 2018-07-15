"""
    controller.sns.photoView.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CloudAlbum is a sample application for TechSummit 2018 workshop.
    Module for OAUTH federation to Twitter.

    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint, request, redirect, url_for, session
from flask import current_app as app
from flask_login import current_user, login_required
from twython import Twython, TwythonError

# from cloudalbum.model.models import db, Photo

from cloudalbum import util
import os
from cloudalbum.config import options

blueprint = Blueprint('twitter', __name__)


@blueprint.route('/twitter/<photo_id>')
@login_required
def send(photo_id):
    """
    Send message and image to Twitter.
    :param photo_id: Target photo id.
    :return: HTML template page for photo list or oauth page.
    """
    if session.__contains__('TWITTER'):
        twitter = session['TWITTER']
        __send_twit__(twitter, photo_id)
        return redirect(url_for('photoView.photos'))
    else:
        # If there is no TWITTER attribute in session, then move to oauth step.
        return __oauth__(photo_id)


def __send_twit__(twitter, photo_id):
    """
    Internal function for send image and message to Twitter
    :param twitter: Session attribute for OAUTH federation with Twitter
    :param photo_id: Target photo id
    :return: None
    """

    try:
        photo = db.session.query(Photo).filter_by(id=photo_id).first()
        path = os.path.join(options['UPLOAD_FOLDER'], util.email_normalize(current_user.email))
        thumbnail = os.path.join(os.path.join(path, "thumbnail"), photo.filename)

        with open(thumbnail, "rb") as file:
            response = twitter.upload_media(media=file)
            twitter.update_status(status=photo.desc,
                                  media_ids=[response['media_id']])
            session['TWITTER_RESULT'] = 'ok'

    except IOError as e:
        app.logger.error("send(): IOError , " + str(e))
        session['TWITTER_RESULT'] = str(e)

    except TwythonError as e:
        app.logger.error("send(): TwythonError , " + str(e))
        session['TWITTER_RESULT'] = str(e)


def __oauth__(photo_id):
    """
    Get oauth token from Twitter
    :param photo_id: target photo id
    :return: oauth URL or photoView.photos view function
    """

    try:
        twitter = Twython(options['TWIT_APP_KEY'],
                          options['TWIT_APP_SECRET'])
        callback_svr = options['TWIT_CALLBACK_SERVER']
        auth = twitter.get_authentication_tokens(
                          callback_url= callback_svr +
                          url_for('twitter.callback', photo_id=photo_id))
        # Keep the temporary authentication token for complete the authentication.
        session['OAUTH_TOKEN'] = auth['oauth_token']
        session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']

    except TwythonError as e:
        app.logger.error("__oauth()__: TwythonError, {0}".format(str(e)))
        session['TWITTER_RESULT'] = str(e)
        return redirect(url_for('photoView.photos'))

    return redirect(auth['auth_url'])


@blueprint.route('/twitter/callback/<photo_id>')
@login_required
def callback(photo_id):
    """
    Callback URL for the authenticated user
    After authentication send image and message to Twitter
    :param photo_id: target photo id
    :return: Redirect HTML template page
    """

    app.logger.info("callback oauth_token:" + request.args['oauth_token']);
    app.logger.info("callback oauth_verifier:" + request.args['oauth_verifier']);

    # Get authentication token from the session attribute
    OAUTH_TOKEN        = session['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = session['OAUTH_TOKEN_SECRET']
    oauth_verifier     = request.args['oauth_verifier']
    
    try:
        # Verify authentication token and create twitter object.
        twitter = Twython(options['TWIT_APP_KEY'],
                          options['TWIT_APP_SECRET'],
                          OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        final_step = twitter.get_authorized_tokens(oauth_verifier)    
        
        # recreate twitter object for final authentication.
        twitter = Twython(options['TWIT_APP_KEY'],
                          options['TWIT_APP_SECRET'],
                          final_step['oauth_token'], 
                          final_step['oauth_token_secret'])
        session['TWITTER'] = twitter
    
        # Send photo image with message to Twitter
        __send_twit__(twitter, photo_id)

    except TwythonError as e:
        app.logger.error("callback(): TwythonError, {0}".format(str(e)))
        session['TWITTER_RESULT'] = str(e)

    return redirect(url_for('photoView.photos'))

