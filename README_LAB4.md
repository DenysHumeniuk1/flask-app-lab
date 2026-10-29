# Лабораторна №4 — продовження lab3

Проєкт побудований безпосередньо на оригінальній гілці `lab3`. Усі попередні маршрути та шаблони збережено. Виправлено точку входу `app.py`: тепер вона використовує Flask-застосунок з пакета `app` та зареєстровані blueprint.

## Запуск (Windows PowerShell)

```powershell
py -m pip install -r requirements.txt
py app.py
```

Відкрийте http://127.0.0.1:5000/users/login

Демонстраційні дані: `student` / `lab4pass` (без бази даних).

## Тести

```powershell
py -m unittest discover -s tests -v
```

## Функціонал

- `/users/login`: GET/POST, flash, сесія;
- `/users/profile`: захищений профіль, таблиця кукі;
- `/users/logout`: POST, вихід;
- `/users/cookies/add`, `/users/cookies/delete`, `/users/cookies/delete-all`: POST;
- `/users/theme/light` і `/users/theme/dark`: POST, тема зберігається у cookie.

Навчальні кукі мають префікс `lab4_`. Видалення всіх стосується кукі лабораторної, щоб не руйнувати Flask-сесію. Cookie теми також відображається у таблиці. Для реального розгортання потрібні захист CSRF, HTTPS, безпечне зберігання паролів та секретний ключ у змінній середовища.
