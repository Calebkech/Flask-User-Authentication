from flask_login import current_user
from flask import redirect, url_for, flash

class AdminRequiredMixin:
    def __init__(self):
        pass
    
    def is_admin_required(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You must be an admin to access this page.", "danger")
            return redirect(url_for("core.home"))  # Redirect to the home page or an appropriate route
        return None  # Continue if the user is an admin
