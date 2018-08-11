import os

conf = {
    # Mandatory variable
    'GMAPS_KEY': os.getenv('GMAPS_KEY', None),

    # Default config values
    'APP_HOST': os.getenv('APP_HOST', '0.0.0.0'),
    'APP_PORT': os.getenv('APP_PORT', 8080),
    'FLASK_SECRET': os.getenv('FLASK_SECRET', os.urandom(24)),
    'SESSION_TIMEOUT': os.getenv('SESSION_TIMEOUT', 30),
    'LOG_FILE_PATH': os.getenv('LOG_FILE_PATH', os.path.join(os.getcwd(), 'logs')),
    'LOG_FILE_NAME': os.getenv('LOG_FILE_NAME', 'cloudalbum.log'),
    'ALLOWED_EXTENSIONS': ['jpg', 'jpeg'],
    'UPLOAD_FOLDER': os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'upload')),
    'LOGGING_FORMAT': os.getenv('LOGGING_FORMAT', '%(asctime)s %(levelname)s: %(message)s in [%(filename)s:%(lineno)d]'),
    'LOGGING_MAX_BYTES': os.getenv('LOGGING_MAX_BYTES', 100000),
    'LOGGING_BACKUP_COUNT': os.getenv('LOGGING_BACKUP_COUNT', 1000),
    'LOGGING_LEVEL': os.getenv('LOGGING_LEVEL', 'debug'),
    'THUMBNAIL_WIDTH': os.getenv('THUMBNAIL_WIDTH', 300),
    'THUMBNAIL_HEIGHT': os.getenv('THUMBNAIL_HEIGHT', 200),

    # DynamoDB
    'AWS_REGION': os.getenv('AWS_REGION', 'ap-southeast-1'),
    'DDB_RCU': os.getenv('DDB_RCU', 10),
    'DDB_WCU': os.getenv('DDB_WCU', 10),

    # S3
    'S3_PHOTO_BUCKET': os.getenv('S3_PHOTO_BUCKET', 'cloudalbum-<initial>'),

    # COGNITO
    'COGNITO_POOL_ID': os.getenv('COGNITO_POOL_ID', '<YOUR_POOL_ID>'),
    'COGNITO_CLIENT_ID': os.getenv('COGNITO_CLIENT_ID', '<YOUR_CLIENT_ID>'),
    'COGNITO_CLIENT_SECRET': os.getenv('COGNITO_CLIENT_SECRET', '<YOUR_CLIENT_SECRET>'),
    'COGNITO_DOMAIN': os.getenv('COGNITO_DOMAIN', '<YOUR_COGNITO_DOMAIN>'),
    'BASE_URL': os.getenv('BASE_URL', '<PREVIEW_URL> or <http://localhost:8080>')
}


