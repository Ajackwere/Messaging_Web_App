from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    message_body = db.Column(db.Text)
    status = db.Column(db.String(20), default='unassigned')


    def __repr__(self):
        return f'<Message {self.id} - Status: {self.status}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'message_body': self.message_body,
            'status': self.status,
        }