"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, connect_db
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


class MessageModelTestCase(TestCase):
    def setUp(self):

        Message.query.delete()
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        m1 = Message(text="message_1_content")
        u1.messages.append(m1)

        m2 = Message(text="message_2_content")
        u2.messages.append(m2)

        db.session.commit()
        self.m1_id = m1.id
        self.m2_id = m2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_message_repr(self):

        m1 = Message.query.get(self.m1_id)

        self.assertEqual(
            repr(m1), f"<Message #{m1.id}: User #{m1.user_id}>")

    def test_valid_message(self):

        u1 = User.query.get(self.u1_id)
        m3 = Message(text='m3_test_text')
        u1.messages.append(m3)
        db.session.commit()

        self.assertTrue(Message.query.get(m3.id))

    def test_invalid_message(self):

        u1 = User.query.get(self.u1_id)
        m3 = Message(text=None)
        u1.messages.append(m3)

        self.assertRaises(IntegrityError, db.session.commit)

    def test_cannot_like_own_msg(self):
        u1 = User.query.get(self.u1_id)
        m1 = Message.query.get(self.m1_id)

        self.assertFalse(u1.can_like_msg(m1))

    def test_can_like_msg(self):
        u1 = User.query.get(self.u1_id)
        m2 = Message.query.get(self.m2_id)

        self.assertTrue(u1.can_like_msg(m2))

    def test_like_msg(self):
        u1 = User.query.get(self.u1_id)
        m2 = Message.query.get(self.m2_id)

        u1.toggle_like(m2)
        db.session.commit()

        self.assertTrue(m2 in u1.liked_messages)

    def test_unlike_msg(self):
        u1 = User.query.get(self.u1_id)
        m2 = Message.query.get(self.m2_id)

        u1.liked_messages.append(m2)
        db.session.commit()

        self.assertFalse(m2 not in u1.liked_messages)

        u1.toggle_like(m2)
        db.session.commit()

        self.assertTrue(m2 not in u1.liked_messages)
