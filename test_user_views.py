

"""User model tests."""


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes, connect_db
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()


# AUTHENTICATION


    def test_following_page_authorized(self):
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u1_id

        response = self.client.get(
            f'/users/{self.u1_id}/following', follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Following page for integration testing", html)

    def test_following_page_unauthorized(self):

        response = self.client.get(
            f'/users/{self.u1_id}/following')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/")

    def test_followers_page_authorized(self):
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u1_id

        response = self.client.get(
            f'/users/{self.u1_id}/followers', follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Followers page for integration testing", html)


# WHEN LOGGED in - can see follower/following pages for any user

# log in
# navigate to random user
# follow route > following LOGGED IN
# check 200
# check DOM
