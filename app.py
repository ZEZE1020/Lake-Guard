import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Fishermen, Fishmongers, LawEnforcers, SystemAdmins

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

API_KEY = 'vai-q1i8N7YR42ML78MkPAyp357B2Yp5i74i'
BASE_TRANSLATE_URL = 'https://api.vambo.ai/v1/translate/text'
BASE_IDENTIFY_URL = 'https://api.vambo.ai/v1/identify/text'

def get_final_url(base_url):
    return f'{base_url}?api_key={API_KEY}'

def translate_text(text, target_lang):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    payload = {
        'text': text,
        'source_lang': 'eng',
        'target_lang': target_lang
    }
    final_url = get_final_url(BASE_TRANSLATE_URL)
    response = requests.post(final_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('translated_text')
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return 'Translation failed'

def identify_lang(text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    payload = {'text': text}
    final_url = get_final_url(BASE_IDENTIFY_URL)
    response = requests.post(final_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('lang')
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return 'Language identification failed'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/translate')
@login_required
def translate():
    return render_template('translate.html')

@app.route('/api/translate', methods=['POST'])
@login_required
def api_translate():
    data = request.json
    text = data.get('text')
    target_lang = data.get('lang')
    translated_text = translate_text(text, target_lang)
    return jsonify({'translated_text': translated_text})

@app.route('/api/identify_lang', methods=['POST'])
@login_required
def api_identify_lang():
    data = request.json
    text = data.get('text')
    lang = identify_lang(text)
    return jsonify({'lang': lang})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        new_user = User(username=username, email=email, password=password, role=role)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Email address already in use. Please use a different email.')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('translate'))  # Redirect to translate page after login
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
