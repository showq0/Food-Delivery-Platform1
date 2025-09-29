from flask import Blueprint
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_socketio import join_room, emit
from .models import db, Chat, Message
from feature1.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db, jwt, bcrypt, socketio

chat_bp = Blueprint('chat', __name__, template_folder='templates')


@chat_bp.route('/chat_room/<int:chat_id>/')
@jwt_required()
def chat_room(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.id).all()
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    # check authrization 
    if user.role == "agent":
        if chat.agent != user:
            return {"msg": "Access denied"}, 403
    if user.role == "customer":
        if chat.customer != user:
            return {"msg": "Access denied"}, 403

    return render_template('chat_room.html', chat=chat, messages=messages, user=user)


@chat_bp.route('/agents')
def agents():
    agents = User.query.filter(User.role == "agent").all()
    return render_template('agents.html', agents=agents)


@chat_bp.route('/create_chat', methods=['POST'])
@jwt_required()
def create_chat():
    current_user_id = int(get_jwt_identity())
    agent_id = int(request.form['agent_id'])
    chat = Chat.query.filter_by(agent_id=agent_id, customer_id=current_user_id).first()

    if not chat:
        chat = Chat(agent_id=agent_id, customer_id=current_user_id)
        db.session.add(chat)
        db.session.commit()
    return redirect(url_for("chat.chat_room", chat_id=chat.id))


# handle chat

@socketio.on('join')
def handle_join(data):
    chat_id = data['chat_id']
    room = f'chat_{chat_id}'
    join_room(room)


@socketio.on('typing')
def handle_typing(data):
    room = f'chat_{data["chat_id"]}'
    emit('typing', {
        'sender_name': data['sender_name'],
        'sender_id': data['sender_id'],
        'typing_status': data['typing_status']
    }, to=room, include_self=False)


@socketio.on('message')
def handle_message(data):
    chat_id = data['chat_id']
    sender_id = data['sender_id']
    content = data['message']

    message = Message(chat_id=chat_id, sender_id=sender_id, content=content)
    db.session.add(message)
    db.session.commit()

    room = f'chat_{chat_id}'
    emit('message', {
        'event_type': 'message',
        'sender_name': data['sender_name'],
        'sender_id': sender_id,
        'message': content
    }, to=room)
