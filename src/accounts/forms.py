from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional

from src.accounts.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    amount = IntegerField(
        "Amount", validators=[DataRequired(), NumberRange(min=1, message="Amount must be at least 1")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    """
    created_by = StringField(
        "Created By", validators=[DataRequired(), Length(min=4, max=25)]
        )
    """
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    expiry_days = IntegerField(
        "Account Expiry (days)",
        validators=[Optional(), NumberRange(min=1, message="Days must be at least 1")],
        default=30  # Default value is 30 days
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        # Check if email is already registered
        user_by_email = User.query.filter_by(email=self.email.data).first()
        if user_by_email:
            self.email.errors.append("Email already registered")
            return False

        # Check if username is already taken
        user_by_username = User.query.filter_by(username=self.username.data).first()
        if user_by_username:
            self.username.errors.append("Username already taken")
            return False

        # Check if passwords match
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False

        return True

class UpdateForm(FlaskForm):
    email = EmailField(
        "Email", validators=[Optional(), Email(message=None), Length(min=6, max=40)]
    )
    username = StringField(
        "Username", validators=[Optional(), Length(min=4, max=25)]
    )
    password = PasswordField(
        "New Password", validators=[Optional(), Length(min=6, max=25)]
    )
    confirm_password = PasswordField(
        "Repeat New Password",
        validators=[
            Optional(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    amount = IntegerField(
        "Amount", validators=[Optional(), NumberRange(min=0, message="Amount must be at least 0")]
    )
    expiry_days = IntegerField(
        "Account Expiry (days)",
        validators=[Optional(), NumberRange(min=1, message="Days must be at least 1")],
    )

    def validate(self):
        initial_validation = super(UpdateForm, self).validate()
        if not initial_validation:
            return False

        # Check if email is already registered (if email is being updated)
        if self.email.data:
            user_by_email = User.query.filter_by(email=self.email.data).first()
            if user_by_email and user_by_email.id != self.id:
                self.email.errors.append("Email already registered")
                return False

        # Check if username is already taken (if username is being updated)
        if self.username.data:
            user_by_username = User.query.filter_by(username=self.username.data).first()
            if user_by_username and user_by_username.id != self.id:
                self.username.errors.append("Username already taken")
                return False

        # Check if passwords match (if password is being updated)
        if self.password.data and self.password.data != self.confirm_password.data:
            self.password.errors.append("Passwords must match")
            return False

        return True
