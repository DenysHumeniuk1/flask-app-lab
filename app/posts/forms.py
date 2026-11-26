from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, BooleanField, SelectField,
    SelectMultipleField, SubmitField,
)
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("Текст публікації", validators=[DataRequired()])
    enabled = BooleanField("Активний пост", default=True)
    publish_date = DateTimeLocalField(
        "Дата та час публікації",
        format="%Y-%m-%dT%H:%M",
        validators=[Optional()],
        render_kw={"type": "datetime-local"},
    )
    category = SelectField(
        "Категорія",
        choices=[
            ("news", "Новина"),
            ("publication", "Публікація"),
            ("tech", "Технології"),
            ("other", "Інше"),
        ],
        validators=[DataRequired()],
    )
    author_id = SelectField("Автор", coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField("Теги", coerce=int, validators=[Optional()])
    submit = SubmitField("Зберегти")
