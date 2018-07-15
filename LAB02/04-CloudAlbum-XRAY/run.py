from flask import Flask
from cloudalbum import application as CloudAlbum
from cloudalbum.config import options
from cloudalbum import util

from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware


app = Flask(__name__)

if __name__ == '__main__':
    util.check_variables()

    app = CloudAlbum.init_app(app)

    ### x-ray set up
    plugins = ('EC2Plugin',)
    xray_recorder.configure(service='MyApplication', plugins=plugins)
    XRayMiddleware(app, xray_recorder)
    patch_all()

    app.logger.debug('DB_URL: {0}'.format(options['DB_URL']))
    app.logger.debug('GMAPS_KEY: {0}'.format(options['GMAPS_KEY']))

    app.run(host=options['APP_HOST'], port=options['APP_PORT'], debug=True)


