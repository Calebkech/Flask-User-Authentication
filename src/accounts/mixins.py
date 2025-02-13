from flask import abort
from flask_login import current_user

class AdminRequiredMixin:
    def is_admin(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return False  # User is not admin
        return True  # User is admin
