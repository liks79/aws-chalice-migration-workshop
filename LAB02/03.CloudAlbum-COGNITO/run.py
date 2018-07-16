from flask import Flask
from cloudalbum import application as CloudAlbum
from cloudalbum.config import conf
from cloudalbum import util

app = Flask(__name__)

if __name__ == '__main__':
    util.check_variables_gmaps()

    app = CloudAlbum.init_app(app)
    app.logger.debug('GMAPS_KEY: {0}'.format(conf['GMAPS_KEY']))

    app.run(host=conf['APP_HOST'], port=conf['APP_PORT'], debug=True)


