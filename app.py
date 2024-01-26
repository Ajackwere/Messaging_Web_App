from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from models import Message, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@app.route('/respond/<int:message_id>', methods=['GET', 'POST'])
def respond(message_id):
    message = db.session.get(Message, message_id)

    if request.method == 'POST':
        response = request.form['response']
        message.message_body += f'\n Agent Response: {response}'
        db.session.commit()

    return render_template('respond.html', message=message)

@app.route('/assign/<int:message_id>', methods=['GET', 'POST'])
def assign_message(message_id):
    if request.method == 'GET':
        message = db.session.get(Message, message_id)
        if message:
            return jsonify({'status': 'success', 'message_status': message.status}), 200
        else:
            return jsonify({'status': 'error', 'message': f'Message {message_id} not found.'}), 404

    elif request.method == 'POST':
        message = db.session.get(Message, message_id)
        if message:
            if message.status == 'unassigned':
                message.status = 'assigned'
                db.session.commit()
                return jsonify({'status': 'success', 'message': f'Message {message_id} assigned successfully.'}), 200
            else:
                return jsonify({'status': 'error', 'message': f'Message {message_id} is already assigned.'}), 400
        else:
            return jsonify({'status': 'error', 'message': f'Message {message_id} not found.'}), 404

@app.route('/claim/<int:message_id>', methods=['POST'])
def claim_message(message_id):
    try:
        message = Message.query.get(message_id)
        if message.status == 'unassigned':
            message.status = 'assigned'
            db.session.commit()
            return jsonify({'status': 'success', 'message': f'Message {message_id} claimed successfully.'}), 200
        else:
            return jsonify({'status': 'error', 'message': f'Message {message_id} is already assigned.'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)