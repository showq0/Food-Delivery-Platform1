from flask import Blueprint, Response, render_template, request, json
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db, r
from feature1.models import User
from feature2.models import Order
import time

notific_bp = Blueprint('notification', __name__, template_folder='templates')


@notific_bp.route('/<int:restaurant_id>')
def dashboard(restaurant_id):
    pending_orders = Order.query.filter_by(
        restaurant_id=restaurant_id,
        status='confirmed'
    ).all()

    orders_data = [
        {"id": o.id, "name": o.customer.username}
        for o in pending_orders
    ]
    return render_template('dashboard.html', restaurant_id=restaurant_id, orders_data=orders_data)


@notific_bp.route("/stream/<int:restaurant_id>")
def stream(restaurant_id):
    def event_stream():
        pubsub = r.pubsub()
        pubsub.subscribe(f"restaurant:{restaurant_id}")
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'].decode())
                order = f"Order: {data['id']}: {data['name']}"
                yield f"data: {order}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


# order from restaurant
@notific_bp.route('/menu/<int:restaurant_id>', methods=["GET"])
def menu(restaurant_id):
    return render_template("restaurant_menu.html", restaurant_id=restaurant_id)


@notific_bp.route('/order', methods=['GET', 'POST'])
@notific_bp.route('/order/<int:id>', methods=['GET'])
@jwt_required()
def order_view(id=None):
    if request.method == "POST":
        current_user_id = int(get_jwt_identity())
        data = request.form

        user = User.query.get(current_user_id)
        print(data.get('restaurant_id'))
        order = Order(customer=user, restaurant_id=int(data['restaurant_id']), status="confirmed")
        db.session.add(order)
        db.session.commit()
        order_data = json.dumps({"id": order.id, "name": order.customer.username})

        r.publish(f"restaurant:{data['restaurant_id']}", order_data)

        return {"msg": "Order sent successfully"}, 200
    if request.method == "GET" and id:
        order = Order.query.get_or_404(id)
        return {"msg": "Order sent successfully",
                'Order': order.restaurant_id,
                'customer': order.customer.username}

    return {"msg": ""}
