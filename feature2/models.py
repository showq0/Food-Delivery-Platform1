from app.extensions import db
from datetime import datetime



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    restaurant_id = db.Column(db.Integer , db.ForeignKey('restaurant.id'),  nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmed')

    customer = db.relationship('User', foreign_keys=[customer_id], backref='orders')
    driver = db.relationship('User', foreign_keys=[driver_id], backref='orders_as_driver')
    restaurant = db.relationship('Restaurant', foreign_keys=[restaurant_id],  backref='orders_as_restaurant')