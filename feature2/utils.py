import queue

sse_connections = {}

def connect_sse(order_id):
    if order_id not in sse_connections:
        sse_connections[order_id] = queue.Queue()
    return sse_connections[order_id]


def push_event(order_id, data):
    if order_id in sse_connections:
        sse_connections[order_id].put(data)

def is_connected(order_id):
    return order_id in sse_connections

def end_connection(order_id):
    if order_id in sse_connections:
        del sse_connections[order_id]
