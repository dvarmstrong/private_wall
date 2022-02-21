
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
        self.reciever = data['reciever']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def create_message(cls,data):
        query = "INSERT into messages (sender_id, sender, reciever_id, reciever, messages) VALUES ( %(id)s, %(sender)s, %(reciever_id)s, %(reciever)s, %(message)s);"

        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def read_message(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as reciever, messages FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 on users2.id = messages.reciever_id WHERE users2.id = %(id)s "

        results = connectToMySQL(cls.db_name).query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
            
        return messages



    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
