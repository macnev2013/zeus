import jwt
from flask import current_app
from time import time
from flask_login import UserMixin, current_user
from zeus import db, login
import logging

LOGGER = logging.getLogger(__name__)


class UptimeWebsiteDetails(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, db.ForeignKey('user.username'))
    website = db.Column(db.String(3000), index=True)

    def add_website(username, website):
        """
        adds website to the databse
        """
        website = UptimeWebsiteDetails(username=current_user.username, website=website)
        db.session.add(website)
        db.session.commit()

    def delete_website(id):
        """
        deletes website from the database
        """
        website = UptimeWebsiteDetails.query.filter_by(id=id).first()
        db.session.delete(website)
        db.session.commit()

    def get_websites_for_user(username):
        """
        lists website for the specific user
        """
        websites = (UptimeWebsiteDetails.query
            .with_entities(UptimeWebsiteDetails.id, UptimeWebsiteDetails.website)
            .filter_by(username=current_user.username).all())
        return websites