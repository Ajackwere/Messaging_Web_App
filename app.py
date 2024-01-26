from flask import Flask, render_template, request

from models import Message, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@app.route('/respond/<int:message_id>', methods=['GET', 'POST'])
def respond(message_id):
    message = Message.query.get(message_id)

    if request.method == 'POST':
        response = request.form['response']
        message.message_body += f'\n Agent Response: {response}'
        db.session.commit()

    return render_template('respond.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)