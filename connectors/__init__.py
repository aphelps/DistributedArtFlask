from flask import current_app
from functools import wraps

from client import Client, ClientDisconnectedException
from state import ModuleState


def connected(f):
    """
    Decorator for functions that require a connected client.  This will
    create the client and module state and ensure that the client is
    connected.
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        if current_app.client is None:

            print("* Initializing app's client and state")
            current_app.client = Client(address=current_app.config["DISTRIBUTED_SERVER_ADDRESS"],
                                        verbose=True)
            current_app.state = ModuleState(current_app.client)

        if not current_app.client.is_connected():
            # The client isn't connected, attempt to connect now
            if not current_app.client.connect():
                raise ClientDisconnectedException("Could not connect to client")

            # Since the client was just connected (possible re-connected) reset
            # the state object
            current_app.state.reset()

        return f(*args, **kwargs)
    return decorated
