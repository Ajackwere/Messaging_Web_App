import csv
from datetime import datetime
from flask import Flask
from models import db, Message
from app import app

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)
def convert_to_datetime(timestamp_str):
    return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

def import_data():
    with app.app_context():
        data = read_csv('GeneralistRails_Project_MessageData.csv')

        for row in data:
            user_id = int(row['UserID'])
            timestamp = convert_to_datetime(row['Timestamp'])
            message_body = row['MessageBody']

            message = Message(user_id=user_id, timestamp=timestamp, message_body=message_body)
            db.session.add(message)

        db.session.commit()
        print("Nimemaliza kuimport data yiotee.")

if __name__ == '__main__':
    import_data()