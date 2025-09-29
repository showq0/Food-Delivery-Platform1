from flask import Blueprint, render_template, request, redirect, url_for, Response
from .models import Order
from feature1.models import User
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import time
import datetime
from .utils import connect_sse, push_event, is_connected, end_connection

order_bp = Blueprint('order', __name__, template_folder='templates')


@order_bp.route('/')
def get_users():
    return {"message": "List of orders"}


@order_bp.route('/menu')
def menu():
    return render_template("menu.html")


# show track page after order is placed
@order_bp.route('/order', methods=['GET', 'POST'])
@order_bp.route('/order/<int:id>', methods=['GET'])
@jwt_required()
def order_view(id=None):
    if request.method == "POST":
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        order = Order(customer=user, status="confirmed")
        db.session.add(order)
        db.session.commit()
        return render_template("track_order.html", order_id=order.id)
    if request.method == "GET" and id:
        order = Order.query.get_or_404(id)
        return render_template("track_order.html", order_id=order.id)

    return redirect(url_for("order.menu"))


@order_bp.route("/sse/<int:order_id>")
def sse_stream(order_id):
    # create SSE connection in memory push event to the queue
    q = connect_sse(order_id)

    def event_stream():
        while True:
            if not q.empty():
                status = q.get()
                yield f"data: {status} and\n\n"
                if status == "delivered":
                    end_connection(order_id)
                    break
            yield f"heartbeat for order {order_id}\n\n"
            time.sleep(15)

    return Response(event_stream(), mimetype="text/event-stream")


@order_bp.route('/order-status/<int:order_id>/', methods=['GET', 'POST'])
def order_status(order_id):
    order = Order.query.get(order_id)
    if not order:
        return "Order not found", 404

    if request.method == 'POST':
        new_status = request.form.get("status")
        order.status = new_status
        db.session.commit()
        # after adding status add the status to the queue if there is a connection
        if is_connected(order.id):
            push_event(order_id, new_status)
        return redirect(url_for('order.order_status', order_id=order.id))

    return render_template("status_update.html", order=order, order_id=order.id)
