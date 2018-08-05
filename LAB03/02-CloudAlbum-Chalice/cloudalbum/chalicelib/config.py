import os
from chalice import CORSConfig
from jinja2 import Environment, PackageLoader, select_autoescape

conf = {
    # Mandatory variable
    'GMAPS_KEY': os.getenv('GMAPS_KEY', ''),

    # Default config values
    'PER_PAGE': os.getenv('PER_PAGE', 6),
    'THUMBNAIL_WIDTH': os.getenv('THUMBNAIL_WIDTH', 300),
    'THUMBNAIL_HEIGHT': os.getenv('THUMBNAIL_HEIGHT', 200),

    # DynamoDB
    'AWS_REGION': os.getenv('AWS_REGION', 'ap-southeast-1'),
    'DDB_RCU': os.getenv('DDB_RCU', 10),
    'DDB_WCU': os.getenv('DDB_WCU', 10),

    # S3
    'S3_PHOTO_BUCKET': os.getenv('S3_PHOTO_BUCKET', 'aws-chalice-workshop'),

    # COGNITO
    'COGNITO_POOL_ID': os.getenv('COGNITO_POOL_ID', 'ap-southeast-1_HAm68sUvj'),
    'COGNITO_CLIENT_ID': os.getenv('COGNITO_CLIENT_ID', '2g6s86v4d44ltem6bu9m3rqola'),
    'COGNITO_CLIENT_SECRET': os.getenv('COGNITO_CLIENT_SECRET', 'h8ltda09tdvu7njuba3d2l971d3irj5t9stelllv7tnj36cstn5'),
    'COGNITO_DOMAIN': os.getenv('COGNITO_DOMAIN', 'cloudalbum.auth.ap-southeast-1.amazoncognito.com'),
    'BASE_URL': os.getenv('BASE_URL', 'https://0ty10bfjr0.execute-api.ap-southeast-1.amazonaws.com/api')

}


S3_STATIC_URL = "https://s3-{0}.amazonaws.com/{1}/static".format(conf['AWS_REGION'], conf['S3_PHOTO_BUCKET'])

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['X-Special-Header'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)

env = Environment(
    loader=PackageLoader(__name__, 'chalicelib/templates'),
    autoescape=select_autoescape(['html', 'xml']))

