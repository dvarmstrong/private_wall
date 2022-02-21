from flask import render_template, session , flash, redirect, request
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_app import app 

@app.route('/post_message', methods=['POST'])
def post_message():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'sender_id' : request.form['sender_id'],
        'reciever_id': request.form['reciever_id'],
        'messages': request.form['messages']
    }

    Message.create_message(data)
    return redirect('/dashboard')