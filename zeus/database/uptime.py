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
        if not UptimeWebsiteDetails.query.filter_by(username=username, website=website).first():
            website = UptimeWebsiteDetails(username=username, website=website)
            db.session.add(website)
            db.session.commit()

    def delete_website(user, website):
        """
        deletes website from the database
        """
        website = UptimeWebsiteDetails.query.filter_by(username=user, website=website).first()
        db.session.delete(website)
        db.session.commit()

    def get_websites_for_user(username):
        """
        lists website for the specific user
        """
        return (UptimeWebsiteDetails.query
            .with_entities(UptimeWebsiteDetails.id, UptimeWebsiteDetails.website)
            .filter_by(username=current_user.username).all())
    
def get_websites_for_all():
    """
    lists website for the all user
    """
    return (UptimeWebsiteDetails.query
        .with_entities(UptimeWebsiteDetails.username, UptimeWebsiteDetails.website)
        .all())