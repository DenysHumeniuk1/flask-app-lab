# Лабораторна робота №6 — ORM та CRUD

## Підготовка середовища
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Запуск застосунку
```bash
flask --app run.py run --debug
```

## Міграції бази даних
Після встановлення залежностей:
```bash
flask --app run.py db init
flask --app run.py db migrate -m "Initial migration"
flask --app run.py db upgrade
flask --app run.py db migrate -m "add is_active and author"
flask --app run.py db upgrade
```
Якщо початкова міграція вже створила всі поля моделі `Post`, другу міграцію не потрібно створювати повторно. Команди виконуються послідовно, а не всі одразу.

## Перевірка
```bash
python -m unittest discover -s tests -v
```

Пости доступні за адресою `/post`.
