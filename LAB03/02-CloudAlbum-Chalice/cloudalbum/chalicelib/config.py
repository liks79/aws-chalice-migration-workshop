from chalice import CORSConfig
from chalicelib.util import get_param

conf = {
    # Mandatory variable
    'GMAPS_KEY': get_param('/cloudalbum/GMAPS_KEY'),

    # Default config values
    'THUMBNAIL_WIDTH': get_param('/cloudalbum/THUMBNAIL_WIDTH'),
    'THUMBNAIL_HEIGHT': get_param('/cloudalbum/THUMBNAIL_HEIGHT'),

    # DynamoDB
    'AWS_REGION': get_param('/cloudalbum/AWS_REGION'),
    'DDB_RCU': get_param('/cloudalbum/DDB_RCU'),
    'DDB_WCU': get_param('/cloudalbum/DDB_WCU'),

    # S3
    'S3_PHOTO_BUCKET': get_param('/cloudalbum/S3_PHOTO_BUCKET'),

    # COGNITO
    'COGNITO_POOL_ID': get_param('/cloudalbum/COGNITO_POOL_ID'),
    'COGNITO_CLIENT_ID': get_param('/cloudalbum/COGNITO_CLIENT_ID'),
    'COGNITO_CLIENT_SECRET': get_param('/cloudalbum/COGNITO_CLIENT_SECRET'),
    'COGNITO_DOMAIN': get_param('/cloudalbum/COGNITO_DOMAIN'),
    'BASE_URL': "https://{0}".format(get_param('/cloudalbum/BASE_URL'))
}


S3_STATIC_URL = "https://s3-{0}.amazonaws.com/{1}/static".format(conf['AWS_REGION'], conf['S3_PHOTO_BUCKET'])

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['X-Special-Header'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)



