"""
    model.__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CloudAlbum is a sample application for TechSummit 2018 workshop.

    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute
from cloudalbum.config import conf
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from cloudalbum.model.models_ddb import User
from cloudalbum.model.models_ddb import Photo

if not User.exists():
    User.create_table(read_capacity_units=conf['DDB_RCU'], write_capacity_units=conf['DDB_WCU'], wait=True)
    print('DynamoDB User table created!')

if not Photo.exists():
    Photo.create_table(read_capacity_units=conf['DDB_RCU'], write_capacity_units=conf['DDB_WCU'], wait=True)
    print('DynamoDB Photo table created!')
