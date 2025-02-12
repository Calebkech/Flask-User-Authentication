import datetime
import unittest

from base_test import BaseTestCase
from flask_login import current_user

from src import bcrypt
from src.accounts.models import User


class TestUser(BaseTestCase):
    def test_user_registration(self):
        # Ensure user registration behaves correctly.
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            self.client.post(
                "/register",
                data=dict(
                    username="test", 
                    email="test@user.com", 
                    password="test_user", 
                    confirm="test_user", 
                    expiry_days=30  # Added expiry_days to the registration
                ),
                follow_redirects=True,
            )
            user = User.query.filter_by(email="test@user.com").first()
            self.assertTrue(user.username == "test")
            self.assertTrue(user.id)
            self.assertTrue(user.email == "test@user.com")
            self.assertFalse(user.is_admin)
            # Check if expiry_date is set correctly
            expected_expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
            self.assertTrue(user.expiry_date > expected_expiry_date - datetime.timedelta(minutes=5))
            self.assertTrue(user.expiry_date < expected_expiry_date + datetime.timedelta(minutes=5))

    def test_get_by_id(self):
        # Ensure id is correct for the current/logged in user
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            self.client.post(
                "/login",
                data=dict(username="admin", password="admin_user"),
                follow_redirects=True,
            )
            self.assertTrue(current_user.id == 1)

    def test_created_on_defaults_to_datetime(self):
        # Ensure that registered_on is a datetime
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            self.client.post(
                "/login",
                data=dict(username="admin", email="ad@min.com", password="admin_user"),
                follow_redirects=True,
            )
            user = User.query.filter_by(email="ad@min.com").first()
            self.assertIsInstance(user.created_on, datetime.datetime)

    def test_check_password(self):
        # Ensure given password is correct after unhashing
        user = User.query.filter_by(email="ad@min.com").first()
        self.assertTrue(bcrypt.check_password_hash(user.password, "admin_user"))
        self.assertFalse(bcrypt.check_password_hash(user.password, "foobar"))

    def test_validate_invalid_password(self):
        # Ensure user can't login when the password is incorrect
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            response = self.client.post(
                "/login",
                data=dict(username="admin", password="foo_bar"),
                follow_redirects=True,
            )
        self.assertIn(b"Invalid username and/or password.", response.data)  # Updated expected error message

    def test_user_account_expiry(self):
        # Ensure user account expires correctly after given expiry days
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            self.client.post(
                "/register",
                data=dict(
                    username="expiry_test",
                    email="expiry@user.com",
                    password="expiry_user",
                    confirm="expiry_user",
                    expiry_days=30,  # Adding expiry_days during registration
                ),
                follow_redirects=True,
            )
            user = User.query.filter_by(email="expiry@user.com").first()
            self.assertIsNotNone(user.expiry_date)
            # Ensure the account has an expiry date set correctly.
            expiry_date = user.expiry_date
            self.assertTrue(expiry_date > datetime.datetime.now())
            self.assertTrue(expiry_date < datetime.datetime.now() + datetime.timedelta(days=31))


if __name__ == "__main__":
    unittest.main()
