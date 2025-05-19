from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import joblib
import numpy as np
import pandas as pd
import logging
import os 
import sqlite3
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '123')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'signup.db')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False) 

# Load model and encoders
model_dir = 'model'
try:
    model = joblib.load(os.path.join(model_dir, 'random_forest.pkl'))
    scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
    encoders = {}
    columns = ['Building_type', 'Property_type', 'Climate_type', 'Soil_type', 'Budget', 'Category', 'Location']
    for col in columns:
        encoders[col] = joblib.load(os.path.join(model_dir, f'{col}_encoder.pkl'))
except Exception as e:
    raise Exception(f"Model loading failed: {e}")

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}', message="Password must contain one number, one uppercase, one lowercase letter, and be at least 8 characters")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose another.')

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/", methods=["GET", "POST"])
def index():
    app_debug = app.config.get('DEBUG', False)
    if app_debug:
        session.clear()  

    if 'username' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        user = User.query.filter_by(username=username).first() 

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')

            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('recommendation_page'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('dashboard.html', username=session.get('username'))


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)



@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        new_username = request.form['username']
        new_role = request.form['role']  

        user.username = new_username
        user.role = new_role  
        db.session.commit()
        flash('User updated successfully.', 'success')

        # goes to the admindashboard
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_user.html', user=user)



@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'info')

    return redirect(url_for('admin_dashboard'))


@app.route('/recommendation', methods=['GET'])
def recommendation_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('recommendation.html')

@app.route('/recommend', methods=['POST'])
def recommendation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    input_data = request.json
    try:
        encoded_input = []
        for col in columns:
            value = input_data[col]
            if value not in encoders[col].classes_:
                return jsonify({"error": f"Invalid value for {col}: {value}"}), 400
            encoded_val = encoders[col].transform([value])[0]
            encoded_input.append(encoded_val)

        input_array = pd.DataFrame([encoded_input], columns=columns)
        input_scaled = scaler.transform(input_array)
        recommendation = model.predict(input_scaled)

        return jsonify({"recommendation": recommendation[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0',port=port,debug=True)
