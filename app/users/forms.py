from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from ..extensions import db
from ..posts.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Ім’я користувача", validators=[
        DataRequired(message="Введіть ім’я користувача."),
        Length(min=3, max=80, message="Ім’я має містити від 3 до 80 символів."),
        Regexp(r"^[A-Za-zА-Яа-яІіЇїЄєҐґ0-9_.-]+$", message="Дозволені літери, цифри, крапка, дефіс та підкреслення."),
    ])
    email = StringField("Email", validators=[
        DataRequired(message="Введіть email."),
        Email(message="Введіть коректну електронну адресу."),
        Length(max=120),
    ])
    password = PasswordField("Пароль", validators=[
        DataRequired(message="Введіть пароль."),
        Length(min=6, message="Пароль має містити щонайменше 6 символів."),
    ])
    confirm_password = PasswordField("Підтвердження пароля", validators=[
        DataRequired(), EqualTo("password", message="Паролі не збігаються."),
    ])
    submit = SubmitField("Зареєструватися")

    def validate_username(self, field):
        if db.session.query(User.id).filter_by(username=field.data.strip()).first():
            raise ValidationError("Це ім’я користувача вже зайняте.")

    def validate_email(self, field):
        if db.session.query(User.id).filter_by(email=field.data.strip().lower()).first():
            raise ValidationError("Ця електронна адреса вже зареєстрована.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Введіть коректний email.")])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запам’ятати мене")
    submit = SubmitField("Увійти")
