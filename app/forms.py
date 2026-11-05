from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, SelectField, TextAreaField, SubmitField,
    DecimalField, IntegerField
)
from wtforms.validators import (
    DataRequired, Length, Email, NumberRange, Regexp,
    ValidationError, Optional
)

CATEGORIES = [
    ("electronics", "Електроніка"),
    ("clothing", "Одяг"),
    ("home", "Для дому"),
    ("other", "Інше"),
]

class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Введіть ім’я."),
            Length(min=4, max=10, message="Ім’я повинно містити від 4 до 10 символів.")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть email."),
            Email(message="Введіть коректну електронну адресу.")
        ]
    )
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(message="Введіть номер телефону."),
            Regexp(r"^\+380\d{9}$", message="Формат телефону: +380XXXXXXXXX.")
        ]
    )
    subject = SelectField(
        "Subject",
        choices=[
            ("general", "General question"),
            ("support", "Technical support"),
            ("cooperation", "Cooperation"),
            ("other", "Other"),
        ],
        validators=[DataRequired(message="Оберіть тему повідомлення.")]
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Введіть повідомлення."),
            Length(max=500, message="Повідомлення не повинно перевищувати 500 символів.")
        ]
    )
    submit = SubmitField("Send Message")


class ProductForm(FlaskForm):
    name = StringField("Назва", validators=[DataRequired(), Length(min=3, max=120)])
    content = TextAreaField("Опис", validators=[DataRequired(), Length(min=5, max=3000)])
    price = DecimalField("Ціна", places=2, validators=[DataRequired(), NumberRange(min=0.01, message="Ціна має бути додатною.")])
    category = SelectField("Категорія", choices=CATEGORIES, validators=[DataRequired()])
    quantity = IntegerField("Кількість", validators=[DataRequired(), NumberRange(min=0, message="Кількість не може бути від'ємною.")])
    image = FileField("Зображення", validators=[Optional(), FileAllowed(["jpg", "jpeg", "png"], "Дозволені лише PNG, JPG та JPEG.")])
    submit = SubmitField("Зберегти")

    def validate_price(self, field):
        if field.data is not None and round(field.data, 2) != field.data:
            raise ValidationError("Ціна повинна мати не більше двох знаків після коми.")


class DeleteForm(FlaskForm):
    """Форма підтвердження видалення з CSRF-захистом."""
    pass
