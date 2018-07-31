import os

conf = {
    # Mandatory variable
    'GMAPS_KEY': os.getenv('GMAPS_KEY', None),

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


    # COGNITO
    # 'COGNITO_POOL_ID': os.getenv('COGNITO_POOL_ID', 'ap-southeast-1_5x6eQybEP'),
    # 'COGNITO_CLIENT_ID': os.getenv('COGNITO_CLIENT_ID', '8cmphdktfkjl9ki0qeunskqql'),
    # 'COGNITO_CLIENT_SECRET': os.getenv('COGNITO_CLIENT_SECRET', 'bb662c8t5vkh9sveaejdk655uv9bubhjei47n9k8vbsb9ee2iv'),
    # 'COGNITO_DOMAIN': os.getenv('COGNITO_DOMAIN', 'cloudalbum-local.auth.ap-southeast-1.amazoncognito.com'),
    # 'BASE_URL': os.getenv('BASE_URL', 'http://localhost:8000')

}


