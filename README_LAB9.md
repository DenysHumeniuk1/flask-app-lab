# Лабораторна робота №9 — Реєстрація та вхід користувачів

Проєкт продовжує лабораторну роботу №8. Наявні моделі доповнено авторизацією, без повторного створення таблиці `users`.

## Реалізовано

- Flask-Bcrypt: хешування та перевірка паролів.
- Реєстрація з перевіркою формату email та унікальності username/email.
- Вхід за email і паролем.
- Flask-Login: `LoginManager`, `UserMixin`, `user_loader`, `login_user`, `logout_user`.
- Автоматичний вхід після реєстрації.
- Захищені сторінки профілю `/users/account` та списку `/users/all`.
- Перемикання меню залежно від стану авторизації.
- Перелік усіх користувачів та їх кількість.
- Автоматизовані тести для реєстрації, входу, виходу та доступу до сторінок.

## Встановлення

У PowerShell відкрийте папку проєкту та активуйте своє віртуальне середовище:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Якщо віртуального середовища ще немає:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Запуск

```powershell
flask run
```

Сторінки:
- Реєстрація: `http://127.0.0.1:5000/users/register`
- Вхід: `http://127.0.0.1:5000/users/login`
- Профіль: `http://127.0.0.1:5000/users/account`
- Список користувачів: `http://127.0.0.1:5000/users/all`

## Перевірка хешування через Flask shell

```powershell
flask shell
```

```python
from app.posts.models import User
from app.extensions import db

user = User(username="labuser", email="labuser@example.com")
user.set_password("secret123")
db.session.add(user)
db.session.commit()

user.password
user.check_password("secret123")
```

Остання команда має повернути `True`. Пароль у базі зберігається у вигляді хешу, а не відкритим текстом. Створювати користувача через shell потрібно лише якщо такого email/username ще немає.

## Тести

```powershell
pytest -q
```

Тести створюють окрему тимчасову SQLite-базу в пам'яті та не змінюють робочу базу проєкту.

## Git: створення гілки lab9

Спочатку перевірте, що робоче дерево попередньої лабораторної чисте:

```powershell
git status
git branch
```

Перейдіть на гілку попередньої лабораторної та створіть нову:

```powershell
git switch lab8
git pull
git switch -c lab9
```

Після перевірки роботи:

```powershell
git add .
git commit -m "Complete lab 9 user registration and authentication"
git push -u origin lab9
```

Якщо ваша гілка попередньої лабораторної має іншу назву, замініть `lab8` на її фактичну назву. Не виконуйте `git pull` або перемикання гілок, якщо у вас є незбережені зміни — спочатку перевірте `git status`.
