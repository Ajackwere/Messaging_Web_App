from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    timestamp = db.Column(db.Datetime, server_default=db.func.now())
    message_body = db.Column(db.Text)

    def __repr__(self):
        return f'<Message {self.id} - Status: {self.status}>'
    