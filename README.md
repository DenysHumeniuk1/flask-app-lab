# Лабораторна робота №2 — Маршрутизація та шаблони

Дві сторінки Flask: «Резюме» (`/resume` або `/`) і «Контакти» (`/contacts`).

## Запуск у PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Відкрийте http://127.0.0.1:5000/ у браузері.

## Git

```powershell
git switch -c lab2
git add .
git commit -m "Implement Flask resume and contacts pages"
```

Якщо гілка `lab2` вже існує, замість `git switch -c lab2` використайте `git switch lab2`.

Форма контактів демонстраційна, не зберігає і не відправляє дані. Зображення — SVG-ілюстрація, яку можна замінити власним фото.
