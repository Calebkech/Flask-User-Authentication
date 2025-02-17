from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import login_required, login_user, logout_user, current_user

from src import bcrypt, db
from src.accounts.models import User

from .forms import LoginForm, RegisterForm, UpdateForm
from datetime import timedelta, datetime

from .mixins import AdminRequiredMixin

accounts_bp = Blueprint("accounts", __name__)


from datetime import datetime, timedelta
from flask import request, redirect, url_for, flash, render_template
from flask_login import current_user
from src.accounts.forms import RegisterForm
from src.accounts.models import User
from src import db

@accounts_bp.route('/register', methods=["GET", "POST"])
def register():
    # Ensure that only admins can access the registration page
    admin_check = AdminRequiredMixin().is_admin()
    if not admin_check:  # If not an admin, trigger 404
        abort(404)  # This will render your 404 error page

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        try:
            # Calculate the expiry date based on the form input
            expiry_date = datetime.now() + timedelta(days=form.expiry_days.data) if form.expiry_days.data else None

            # Create a new user
            user = User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
                amount=form.amount.data,  # Add the amount field
                created_by=current_user.username,  # Set created_by to the logged-in admin
                expiry_date=expiry_date  # Store the expiry date in the database
            )

            db.session.add(user)
            db.session.commit()

            flash("User registered successfully!", "success")
            return redirect(url_for("core.home"))

        except Exception as e:
            db.session.rollback()  # Rollback the transaction if an error occurs
            flash(f"An error occurred while registering: {str(e)}", "danger")
            return render_template("accounts/register.html", form=form)

    return render_template("accounts/register.html", form=form)

@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    
    form = LoginForm(request.form)
    if form.validate_on_submit():
        try:
            # Query the user by username
            user = User.query.filter_by(username=form.username.data).first()
            
            if user:
                # Check if the password matches
                is_password_correct = bcrypt.check_password_hash(user.password, form.password.data)
                
                if is_password_correct:
                    # Check if the user's account is expired
                    if user.expiry_date and user.expiry_date < datetime.now():
                        flash("Your account has expired.", "danger")
                        return render_template("accounts/login.html", form=form)
                    
                    # Log the user in if everything is valid
                    login_user(user)
                    flash("Login successful!", "success")
                    return redirect(url_for("core.home"))
                else:
                    flash("Invalid username and/or password.", "danger")
            else:
                flash("Invalid username and/or password.", "danger")
            
        except Exception as e:
            flash(f"An error occurred while logging in: {str(e)}", "danger")
            return render_template("accounts/login.html", form=form)
    
    return render_template("accounts/login.html", form=form)

@accounts_bp.route('/users', methods=["GET"])
@login_required
def list_users():
    # Ensure that only admins can access this route
    if not current_user.is_admin:
        abort(404)  # page not found for non-admin users

    # Fetch all users from the database
    users = User.query.all()

    # Render the template with the list of users
    return render_template("accounts/list_users.html", users=users)

@accounts_bp.route('/update/<user_id>', methods=["GET", "POST"])
@login_required
def update_user(user_id):
    # Ensure that only admins can access this route
    if not current_user.is_admin:
        abort(404)  # 404 access for non-admin users

    # Fetch the user to be updated
    user_to_update = User.query.get_or_404(user_id)

    # Initialize the form with the user's current data and pass the user_id
    form = UpdateForm(user_id=user_to_update.id, obj=user_to_update)

    if form.validate_on_submit():
        try:
            # Update email if provided
            if form.email.data:
                user_to_update.email = form.email.data

            # Update username if provided
            if form.username.data:
                user_to_update.username = form.username.data

            # Update password if provided
            if form.password.data:
                user_to_update.password = bcrypt.generate_password_hash(form.password.data)

            # Update amount if provided
            if form.amount.data is not None:
                user_to_update.amount = form.amount.data

            # Update expiry date if provided
            if form.expiry_days.data:
                user_to_update.expiry_date = datetime.now() + timedelta(days=form.expiry_days.data)

            # Update created_by if provided (admin-only field)
            if current_user.is_admin and form.created_by.data:
                user_to_update.created_by = form.created_by.data

            # Commit changes to the database
            db.session.commit()

            flash("User updated successfully!", "success")
            return redirect(url_for("accounts.list_users", user_id=user_to_update.id))

        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            flash(f"An error occurred while updating the user: {str(e)}", "danger")
            return render_template("accounts/update_user.html", form=form, user=user_to_update)

    return render_template("accounts/update_user.html", form=form, user=user_to_update)

@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))

@accounts_bp.route('/terms')
def terms():
    return render_template('accounts/terms.html')