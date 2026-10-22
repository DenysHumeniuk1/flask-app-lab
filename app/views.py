from flask import render_template, request
from . import app

@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    submitted = request.method == 'POST'
    return render_template('contacts.html', title='Контакти', submitted=submitted)

@app.route('/homepage')
def home():
    return render_template('homepage.html', title='Головна', agent=request.user_agent)
