import time

from hmtl.client import HMTLClient
import hmtl.HMTLprotocol as HMTLprotocol
from hmtl.TrianglePrograms import TriangleSnake,TriangleStatic
from state import State

server_client = None


def get_client(address):
    """Get a singleton device client"""
    global server_client
    if server_client is None:
        server_client = Client(address=address, verbose=True)
    return server_client


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

        # Attempt to connect to the address
        self.connect()

        self.state = State()

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

    def send_msg(self, msg, expect_response=False):
        start_time = time.time()
        self.hmtl_client.send_and_ack(msg, expect_response)
        end_time = time.time()
        print("Client: sent and acked in %.6fs" % (end_time - start_time))

    def is_connected(self):
        return self.hmtl_client is not None

    def is_cleared(self):
        return self.cleared

    def send_clear_programs(self):
        print("Client: Sending command to clear all programs")
        self.send_msg(
            HMTLprotocol.get_program_none_msg(HMTLprotocol.BROADCAST,
                                              HMTLprotocol.OUTPUT_ALL_OUTPUTS)
        )
        self.cleared = True
        return True

    def send_rgb(self, red, green, blue):
        if not self.is_connected():
            print("ERROR: Client is not connected")
            return False

        if not self.is_cleared():
            self.send_clear_programs()

        print("Client: sending rgb %f,%f,%f" % (red, green, blue))

        self.send_msg(
            HMTLprotocol.get_rgb_msg(HMTLprotocol.BROADCAST,
                                     HMTLprotocol.OUTPUT_ALL_OUTPUTS,
                                     red, green, blue)
        )

        return True

    def send_snake(self, bg, period, colormode):
        print("Client: sending snake bg:%s period:%d, mode:%d" % (bg, period, colormode))
        snake = TriangleSnake(period, bg, colormode)
        self.send_msg(
            snake.msg(HMTLprotocol.BROADCAST,
                      HMTLprotocol.OUTPUT_ALL_OUTPUTS)
        )
        return True
