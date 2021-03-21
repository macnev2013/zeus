import jwt
from flask import current_app
from time import time
from flask_login import UserMixin
from zeus import db, login
import logging

LOGGER = logging.getLogger(__name__)


class UptimeWebsiteDetails(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('user.username'))
    website = db.Column(db.String(3000), index=True)

    # def __repr__(self):
    #     return self.website

    def get_websites(self, username):
        websites = UptimeWebsiteDetails.query.filter_by(username=username).all()
        print(websites)
        return websites