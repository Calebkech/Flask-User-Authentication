import unittest
from datetime import datetime, timedelta
from base_test import BaseTestCase
from flask_login import current_user
from src.accounts.models import User
from src import db


class TestPublic(BaseTestCase):
    def test_main_route_requires_login(self):
        # Ensure main route requires a logged-in user.
        response = self.client.get("/", follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertIn(b"Please log in to access this page", response.data)

    def test_logout_route_requires_login(self):
        # Ensure logout route requires a logged-in user.
        response = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"Please log in to access this page", response.data)


class TestLoggingInOut(BaseTestCase):
    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials
        with self.client:
            response = self.client.post(
                "/login",
                data=dict(username="admin", password="admin_user"),
                follow_redirects=True,
            )
            self.assertTrue(current_user.username == "admin")
            self.assertTrue(current_user.is_active)
            self.assertTrue(response.status_code == 200)

    def test_logout_behaves_correctly(self):
        # Ensure logout behaves correctly, regarding the session
        with self.client:
            self.client.post(
                "/login",
                data=dict(username="admin", password="admin_user"),
                follow_redirects=True,
            )
            response = self.client.get("/logout", follow_redirects=True)
            self.assertIn(b"You were logged out.", response.data)
            self.assertFalse(current_user.is_active)

    def test_login_with_expired_account(self):
        # Ensure user with expired account cannot log in
        expired_user = User.query.filter_by(username="expired").first()

        if not expired_user:
            # Create a test user if it doesn't exist
            expired_user = User(
                email="expired@user.com", 
                username="expired", 
                password="expired_user"
            )
            db.session.add(expired_user)
            db.session.commit()

        # Set the expiry date in the past
        expired_user.expiry_date = datetime.now() - timedelta(days=1)  # Expiry date in the past
        db.session.commit()

        with self.client:
            self.client.get("/logout", follow_redirects=True)  # Make sure the user is logged out before the test
            response = self.client.post(
                "/login",
                data=dict(username="expired", password="expired_user"),
                follow_redirects=True,
            )
            self.assertIn(b"Your account has expired.", response.data)  # Ensure expiry message is shown
            self.assertFalse(current_user.is_authenticated)  # Ensure user is not logged in

    def test_login_with_non_expired_account(self):
        # Ensure user with non-expired account can log in successfully
        non_expired_user = User.query.filter_by(username="admin").first()
        non_expired_user.expiry_date = datetime.now() + timedelta(days=30)  # Ensure the user is not expired
        db.session.commit()

        with self.client:
            response = self.client.post(
                "/login",
                data=dict(username="admin", password="admin_user"),
                follow_redirects=True,
            )
            self.assertTrue(current_user.username == "admin")  # Ensure the user is logged in
            self.assertTrue(current_user.is_active)
            self.assertTrue(response.status_code == 200)

if __name__ == "__main__":
    unittest.main()
