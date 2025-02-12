from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from src import bcrypt, db
from src.accounts.models import User

from .forms import LoginForm, RegisterForm
from datetime import timedelta, datetime

from .mixins import AdminRequiredMixin

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    # Ensure that only admins can access the registration page
    admin_check = AdminRequiredMixin().is_admin_required()
    if admin_check:
        return admin_check  # If not an admin, return the redirect

    """
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("core.home"))
    """
    
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        try:
            # Calculate the expiry date
            expiry_date = datetime.now() + timedelta(days=form.expiry_days.data)

            # Create a new user
            user = User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
                expiry_date=expiry_date  # Store the expiry date in the database
            )

            db.session.add(user)
            db.session.commit()

            """
            # Log in the user and flash a success message
            login_user(user)
            flash("You registered and are now logged in. Welcome!", "success")
            """

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


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))
