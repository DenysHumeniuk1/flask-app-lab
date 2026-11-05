from flask import render_template, request, redirect, url_for
from . import user_bp

@user_bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', type=int)
    return render_template('users/hi.html', title='Привітання', name=name, age=age)

@user_bp.route('/admin')
def admin():
    return redirect(url_for('users.greetings', name='administrator', age=45))


# Лабораторна №4: автентифікація, сесії, кукі та теми.
from flask import flash, session, make_response
from datetime import datetime, timezone

DEMO_USERS = {'student': 'lab4pass'}  # заглушка без БД (лише для навчання)
COOKIE_PREFIX = 'lab4_'

def authenticated():
    return bool(session.get('username'))

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if DEMO_USERS.get(username) == password and username in DEMO_USERS:
            session.clear()
            session['username'] = username
            flash('Вхід успішний!', 'success')
            return redirect(url_for('users.profile'))
        flash('Неправильний логін або пароль.', 'danger')
        return redirect(url_for('users.login'))
    return render_template('users/login.html', title='Вхід')

@user_bp.route('/profile')
def profile():
    if not authenticated():
        flash('Спочатку увійдіть у систему.', 'warning')
        return redirect(url_for('users.login'))
    cookies = {k: v for k, v in request.cookies.items() if k.startswith(COOKIE_PREFIX)}
    theme = request.cookies.get('lab4_theme', 'light')
    if theme not in ('light', 'dark'):
        theme = 'light'
    return render_template('users/profile.html', title='Профіль', username=session['username'], cookies=cookies, theme=theme)

@user_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@user_bp.route('/cookies/add', methods=['POST'])
def add_cookie():
    if not authenticated():
        flash('Увійдіть у систему.', 'warning')
        return redirect(url_for('users.login'))
    key = request.form.get('key', '').strip()
    value = request.form.get('value', '')
    try:
        age = int(request.form.get('max_age', '3600'))
    except ValueError:
        age = 0
    if not key or not key.replace('_', '').isalnum() or len(key) > 40 or age < 1 or age > 31536000:
        flash('Ключ: лише літери, цифри й _. Термін: 1–31536000 секунд.', 'danger')
        return redirect(url_for('users.profile'))
    if key in ('theme',) or len(value) > 1000:
        flash('Недопустимий ключ або занадто довге значення.', 'danger')
        return redirect(url_for('users.profile'))
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie(COOKIE_PREFIX + key, value, max_age=age, httponly=True, samesite='Lax')
    flash('Кукі успішно додано.', 'success')
    return response

@user_bp.route('/cookies/delete', methods=['POST'])
def delete_cookie():
    if not authenticated():
        flash('Увійдіть у систему.', 'warning')
        return redirect(url_for('users.login'))
    key = request.form.get('key', '').strip()
    response = make_response(redirect(url_for('users.profile')))
    if key and key not in ('theme',) and COOKIE_PREFIX + key in request.cookies:
        response.delete_cookie(COOKIE_PREFIX + key)
        flash('Кукі видалено.', 'success')
    else:
        flash('Кукі не знайдено або ключ недоступний.', 'warning')
    return response

@user_bp.route('/cookies/delete-all', methods=['POST'])
def delete_all_cookies():
    if not authenticated():
        flash('Увійдіть у систему.', 'warning')
        return redirect(url_for('users.login'))
    response = make_response(redirect(url_for('users.profile')))
    # Видаляємо демонстраційні cookies, а також тему. Сесію не чіпаємо.
    for key in request.cookies:
        if key.startswith(COOKIE_PREFIX):
            response.delete_cookie(key)
    flash('Усі кукі лабораторної видалено.', 'success')
    return response

@user_bp.route('/theme/<theme>', methods=['POST'])
def change_theme(theme):
    if not authenticated():
        flash('Увійдіть у систему.', 'warning')
        return redirect(url_for('users.login'))
    if theme not in ('light', 'dark'):
        flash('Невідома тема.', 'danger')
        return redirect(url_for('users.profile'))
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('lab4_theme', theme, max_age=31536000, httponly=True, samesite='Lax')
    flash('Тему змінено.', 'success')
    return response
