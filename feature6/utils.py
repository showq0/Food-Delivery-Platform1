import queue

sse_connections = []
global_announcment = []


def connect_sse():
    connection_queue = queue.Queue()
    sse_connections.append(connection_queue)
    for announcement in global_announcment:
        # add global announcement to each new connection
        connection_queue.put(announcement)
    return connection_queue


def end_connection(connection_queue):
    sse_connections.remove(connection_queue)


def push_event_all(data):
    for q in sse_connections:
        q.put(data)


def add_global_announcement(data):
    global_announcment.append(data)
    return True
