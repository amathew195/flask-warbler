"""Message model tests."""

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

        self.u1_id = u1.id
        self.u2_id = u2.id

        m1 = Message(text="message_1_content",
                     user_id=self.u1_id
                     )

        m2 = Message(text="message_2_content",
                     user_id=self.u2_id
                     )

        db.session.add_all([m1, m2])
        db.session.commit

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()
