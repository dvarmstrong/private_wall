
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
from flask import render_template, request, session, redirect,flash

bcrypt = Bcrypt(app)






@app.route('/')
def index():
    return render_template('index.html', users=User.get_all_users())


@app.route('/register', methods=['POST'])
def register():

    if not User.validate_user(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data ={
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }

    user_id =User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard.html')    


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    
    #check validations for the user to login 
    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': session['user_id']
    }

    return render_template('dashboard.html', user = User.get_by_id(data), messages= Message.read_message(data), users=User.get_all_users(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
