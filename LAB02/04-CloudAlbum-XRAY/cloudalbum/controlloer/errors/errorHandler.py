"""
    controller.errors.errorHandler.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CloudAlbum is a sample application for TechSummit 2018 workshop.

    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""

from flask import render_template, current_app as app


def not_found(error):
    """
    HTTP 404 not found error handler.
    :param error: specific error object.
    :return:     :return: render 'error.html'render 'error.html' with error message.
    """
    app.logger.error(error)
    return render_template('error.html', err_msg=error.description), 404


def server_error(error):
    """
    General server side error handler.
    :param error: specific error object.
    :return: render 'error.html' with error message.
    """
    message = None
    app.logger.error(error)
    if hasattr(error, 'description'):
        message = error.description
    else:
        message = str(error)
    return render_template('error.html', err_msg=message), 500


def csrf_error(error):
    """
    CSRF error handler
    :param error: specific error object.
    :return: render 'error.html' with error message.
    """
    app.logger.error(error)
    return render_template('error.html', err_msg=error.description), 400
