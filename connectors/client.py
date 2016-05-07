import time

from hmtl.client import HMTLClient


class ClientDisconnectedException(Exception):
    pass


class Client:
    """
    This class controls a connection to a hmtl server as well as tracking
    the state of the devices it is connected to.
    """

    def __init__(self, address, verbose=False):
        self.address = address
        self.hmtl_client = None
        self.verbose = verbose
        self.cleared = False

    def connect(self, force_reconnect = False):
        if self.is_connected() and not force_reconnect:
            print("* Client is already connected")
            return True

        if self.is_connected() and force_reconnect:
            print("* Disconnecting client")
            self.hmtl_client.close()
            self.hmtl_client = None

        try:
            print("* Creating HMTL Client.  address=%s" % self.address)
            self.hmtl_client = HMTLClient(address=self.address,
                                          verbose=self.verbose)
            return True
        except Exception as e:
            print("ERROR: Failed to create client: %s" % e)
            self.hmtl_client = None
            return False

    def is_connected(self):
        return self.hmtl_client is not None

    def send_msg(self, msg, expect_response=False):
        if not self.is_connected():
            raise ClientDisconnectedException("Client is not connected")

        start_time = time.time()
        self.hmtl_client.send_and_ack(msg, expect_response)
        end_time = time.time()
        print("Client: sent and acked in %.6fs" % (end_time - start_time))
