from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{
        "id": message.id,
        "body": message.body,
        "username": message.username,
        "created_at": message.created_at.isoformat() if message.created_at else None,
        "updated_at": message.updated_at.isoformat() if message.updated_at else None
    } for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data.get("body") or not data.get("username"):
        return jsonify({"error": "Both 'body' and 'username' are required"}), 400

    new_message = Message(
        body=data["body"],
        username=data["username"]
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        "id": new_message.id,
        "body": new_message.body,
        "username": new_message.username,
        "created_at": new_message.created_at.isoformat() if new_message.created_at else None,
        "updated_at": new_message.updated_at.isoformat() if new_message.updated_at else None
    }), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()

    if "body" in data:
        message.body = data["body"]

    db.session.commit()

    return jsonify({
        "id": message.id,
        "body": message.body,
        "username": message.username,
        "created_at": message.created_at.isoformat() if message.created_at else None,
        "updated_at": message.updated_at.isoformat() if message.updated_at else None
    }), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)

    db.session.delete(message)
    db.session.commit()

    return jsonify({"message": f"Message {id} deleted successfully"}), 204


@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555)
