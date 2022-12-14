"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


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


class UserModelTestCase(TestCase):
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

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(len(u1.liked_messages), 0)
        self.assertEqual(len(u1.following), 0)

    def test_user_repr(self):
        u1 = User.query.get(self.u1_id)

        self.assertEqual(repr(u1), f"<User #{self.u1_id}: u1, u1@email.com>")

    def test_user_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        u1.following.append(u2)

        self.assertTrue(u1.is_following(u2))

    def test_user_not_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_following(u2))

    def test_user_is_followed_by(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        u2.following.append(u1)

        self.assertTrue(u1.is_followed_by(u2))

    def test_user_is_not_followed_by(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_followed_by(u2))

    def test_valid_signup(self):
        u3 = User.signup("u3", "u3@email.com", "password", None)
        db.session.commit()

        self.assertTrue(User.query.get(u3.id))

    def test_invalid_duplicate_username(self):
        User.signup("u1", "u1@email.com", "password", None)

        self.assertRaises(IntegrityError, db.session.commit)

    def test_invalid_input_signup(self):
        User.signup("u4", None, "password", None)

        self.assertRaises(IntegrityError, db.session.commit)

    def test_authentication_valid(self):

        self.assertTrue(isinstance(User.authenticate(
            username="u1", password="password"), User)
        )

    def test_authentication_invalid_username(self):

        self.assertFalse(User.authenticate(
            username="u7", password="password"))

    def test_authentication_invalid_password(self):

        self.assertFalse(User.authenticate(
            username="u1", password="invalid_password"))
