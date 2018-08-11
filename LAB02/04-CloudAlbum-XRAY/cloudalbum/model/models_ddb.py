
"""
    model.models_ddb.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CloudAlbum is a sample application for TechSummit 2018 workshop.

    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from flask_login import UserMixin
from pynamodb.indexes import GlobalSecondaryIndex, IncludeProjection
from cloudalbum import login
from cloudalbum import util
from cloudalbum.config import conf


class EmailIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        index_name = 'user-email-index'
        read_capacity_units = 2
        write_capacity_units = 1
        projection = IncludeProjection(['password'])

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    email = UnicodeAttribute(hash_key=True)


class User(Model, UserMixin):
    """
    User table for DynamoDB
    """

    class Meta:
        table_name = 'User'
        region = conf['AWS_REGION']

    id = UnicodeAttribute(hash_key=True)
    email_index = EmailIndex()
    email = UnicodeAttribute(null=False)
    username = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)


class Photo(Model):
    """
    User table for DynamoDB
    """

    class Meta:
        table_name = 'Photo'
        region = conf['AWS_REGION']

    user_id = UnicodeAttribute(hash_key=True)
    id = NumberAttribute(range_key=True)
    tags = UnicodeAttribute(null=False)
    desc = UnicodeAttribute(null=False)
    filename_orig = UnicodeAttribute(null=False)
    filename = UnicodeAttribute(null=False)
    filesize = NumberAttribute(null=False)
    geotag_lat = UnicodeAttribute(null=False)
    geotag_lng = UnicodeAttribute(null=False)
    upload_date = UTCDateTimeAttribute(default=util.the_time_now())
    taken_date = UTCDateTimeAttribute(default=util.the_time_now())
    make = UnicodeAttribute(null=True)
    model = UnicodeAttribute(null=True)
    width = UnicodeAttribute(null=False)
    height = UnicodeAttribute(null=False)
    city = UnicodeAttribute(null=True)
    nation = UnicodeAttribute(null=False)
    address = UnicodeAttribute(null=False)


# @login.user_loader
# def load_user(id):
#     """
#     User information loader for authenticated user
#     :param id: user id
#     :return: user record from User table
#     """
#
#     user_item = UserModel.get(id)
#     return user_item
#


