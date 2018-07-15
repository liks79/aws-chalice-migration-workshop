import os

options = {
    # Mandatory variable
    'GMAPS_KEY': os.getenv('GMAPS_KEY', None),
    'DB_URL': os.getenv('DB_URL', None),

    # Default config values
    'APP_HOST': os.getenv('APP_HOST', '0.0.0.0'),
    'APP_PORT': os.getenv('APP_PORT', 8000),
    'FLASK_SECRET': os.getenv('FLASK_SECRET', os.urandom(24)),
    'SESSION_TIMEOUT': os.getenv('SESSION_TIMEOUT', 30),
    'SQLALCHEMY_TRACK_MODIFICATIONS': os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False),
    'DB_ECHO_FLAG': os.getenv('DB_ECHO_FLAG', True),
    'DB_POOL_SIZE': os.getenv('DB_POOL_SIZE', 10),
    'DB_MAX_OVERFLOW': os.getenv('DB_MAX_OVERFLOW', 20),
    'DB_SQLALCHEMY_POOL_TIMEOUT': os.getenv('DB_SQLALCHEMY_POOL_TIMEOUT', 15),
    'DB_SQLALCHEMY_POOL_RECYCLE': os.getenv('DB_SQLALCHEMY_POOL_RECYCLE', 7200),
    'LOG_FILE_PATH': os.getenv('LOG_FILE_PATH', os.path.join(os.getcwd(), 'logs')),
    'LOG_FILE_NAME': os.getenv('LOG_FILE_NAME', 'cloudalbum.log'),
    'ALLOWED_EXTENSIONS': ['jpg', 'jpeg'],
    'UPLOAD_FOLDER': os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'upload')),
    'LOGGING_FORMAT': os.getenv('LOGGING_FORMAT', '%(asctime)s %(levelname)s: %(message)s in [%(filename)s:%(lineno)d]'),
    'LOGGING_MAX_BYTES': os.getenv('LOGGING_MAX_BYTES', 100000),
    'LOGGING_BACKUP_COUNT': os.getenv('LOGGING_BACKUP_COUNT', 1000),
    'LOGGING_LEVEL': os.getenv('LOGGING_LEVEL', 'debug'),
    'PER_PAGE': os.getenv('PER_PAGE', 6),
    'THUMBNAIL_WIDTH': os.getenv('THUMBNAIL_WIDTH', 350),
    'THUMBNAIL_HEIGHT': os.getenv('THUMBNAIL_HEIGHT', 300),

    # DynamoDB
    'AWS_REGION': os.getenv('AWS_REGION', 'ap-southeast-1'),
    'DDB_RCU': os.getenv('DDB_RCU', 10),
    'DDB_WCU': os.getenv('DDB_WCU', 10),

    # For Twitter federation.(Not mandatory)
    'TWIT_APP_KEY':  os.getenv('TWIT_APP_KEY', ''),
    'TWIT_APP_SECRET': os.getenv('TWIT_APP_SECRET', ''),
    'TWIT_CALLBACK_SERVER': os.getenv('TWIT_CALLBACK_SERVER', '')


}


