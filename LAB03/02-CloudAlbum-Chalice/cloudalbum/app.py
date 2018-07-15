from chalice import Chalice

app = Chalice(app_name='cloudalbum')


## SITE ##
@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/callback')
def callback():
    return {'hello': 'world'}


## PHOTO ##
@app.route('/photos')
def photos():
    return {'hello': 'world'}


@app.route('/photos/new')
def upload():
    return {'hello': 'world'}


@app.route('/photos/map')
def map():
    return {'hello': 'world'}

