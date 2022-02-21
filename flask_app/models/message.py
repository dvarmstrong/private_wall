
from pyexpat.errors import messages
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash




class Message:

    db_name = 'private_wall'

    def __init__(self, data):
        self.id = data['id']
        self.messages = data['messages']
        self.reciever_id = data['reciever_id']
        self.reciever = None
        self.sender_id = data['sender_id']
        self.sender = None
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def create_message(cls,data):
        query = "INSERT into messages (sender_id, sender, reciever_id, reciever, messages) VALUES ( %(id)s, %(sender)s, %(reciever_id)s, %(reciever)s, %(message)s);"

        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def read_message(cls, data):
        # query = "SELECT users.first_name as sender, users2.first_name as reciever, messages FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 on users2.id = messages.reciever_id WHERE users2.id = %(id)s; "
        query = "SELECT * FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 on users2.id = messages.reciever_id WHERE users2.id = %(id)s; "

        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        messages = []
        for message in results:
            # make a dictionary for the message
            message_dict = {
                'id':message['messages.id'],
                'messages':message['messages'],
                'sender_id':message['sender_id'],
                'reciever_id':message['reciever_id'],
                'created_at':message['messages.created_at'],
                'updated_at':message['messages.updated_at']
            }
            #make a message object
            this_message = cls(message_dict)
            # make a sender_object
            this_sender = User(message)
            # make a dictionary for the receiver
            r_dictionary = {
                'id':message['users2.id'],
                'first_name':message['users2.first_name'],
                'last_name':message['users2.last_name'],
                'email':message['users2.email'],
                'password':message['users2.password'],
                'created_at':message['users2.created_at'],
                'updated_at':message['users2.updated_at'],
            }
            this_reciever = User(r_dictionary)
            # associate the sender, reiever, and the message
            this_message.sender = this_sender
            this_message.reciever = this_reciever
            messages.append(this_message)
            
        return messages # list of message objects



    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
