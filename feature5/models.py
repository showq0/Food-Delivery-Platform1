from app.extensions import db, bcrypt
from datetime import datetime


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('User', foreign_keys=[customer_id], backref='customer_chats')
    agent = db.relationship('User', foreign_keys=[agent_id], backref='agent_chats')

    __table_args__ = (
        db.UniqueConstraint('agent_id', 'customer_id', name='unique_agent_customer'),
    )

    def __repr__(self):
        return f"<Chat {self.id} between {self.customer.username} and {self.agent.username}>"


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)

    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    chat = db.relationship('Chat', backref='messages')
    sender = db.relationship('User', backref='sent_messages')

    def __repr__(self):
        return f"<Message: {self.content}>"
