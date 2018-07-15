"""
    model.models_ddb.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    CloudAlbum is a sample application for TechSummit 2018 workshop.

    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class User(Model):
    """
    User table for DynamoDB
    """
    class Meta:
        table_name = "User"
        region = "ap-southeast-1"

    id = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute(null=False)
    email = UnicodeAttribute(range_key=True)
    password = UnicodeAttribute(null=False)
    photos = UnicodeAttribute(null=True)

    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<%r %r %r>' % (self.__tablename__, self.username, self.email)


