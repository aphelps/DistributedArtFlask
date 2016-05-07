from flask import current_app
from functools import wraps

from client import Client, ClientDisconnectedException

server_client = None


def get_client():
    """
    Get a singleton device client
    """
    global server_client
    if server_client is None:
        server_client = Client(address=current_app.config["DISTRIBUTED_SERVER_ADDRESS"],
                               verbose=True)
    return server_client


def connected(f):
    """Decorator for functions that require a connected client"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_app.client = get_client()
        if not current_app.client.is_connected():
            if not current_app.client.connect():
                raise ClientDisconnectedException("Could not connect to client")
        return f(*args, **kwargs)
    return decorated
