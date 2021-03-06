import hmtl.HMTLprotocol as HMTLprotocol
from hmtl.TrianglePrograms import TriangleSnake,TriangleStatic

STATE_UNKNOWN = -1
STATE_NONE = 0
STATE_RGB = 1
STATE_SNAKE = 2
STATE_BLINK = 3

def is_program_state(state):
    if state == STATE_RGB:
        return False

    return True


class ModuleState:
    """
    This class tracks the state of a generic connected device.
    """

    def __init__(self, client):
        self.state = STATE_UNKNOWN
        self.client = client
        self.address = HMTLprotocol.BROADCAST

    def reset(self):
        self.state = STATE_UNKNOWN

    def clear(self):
        """Send a message to clear any currently running program"""
        self.client.send_msg(
            HMTLprotocol.get_program_none_msg(self.address,
                                              HMTLprotocol.OUTPUT_ALL_OUTPUTS)
        )
        self.state = STATE_NONE

    def rgb(self, red, green, blue):
        """Set the module to the indicated color"""
        if is_program_state(self.state):
            self.clear()
        self.client.send_msg(
            HMTLprotocol.get_rgb_msg(self.address,
                                     HMTLprotocol.OUTPUT_ALL_OUTPUTS,
                                     red, green, blue)
        )
        self.state = STATE_RGB

    def blink(self, on_period, on_color, off_period, off_color):
        self.client.send_msg(
            HMTLprotocol.get_program_blink_msg(self.address,
                                     HMTLprotocol.OUTPUT_ALL_OUTPUTS,
                                               on_period,
                                               on_color,
                                               off_period,
                                               off_color)
        )
        self.state = STATE_BLINK

    def snake(self, bg, period, colormode):
        snake = TriangleSnake(period, bg, colormode)
        self.client.send_msg(
            snake.msg(self.address,
                      HMTLprotocol.OUTPUT_ALL_OUTPUTS)
        )

        self.state = STATE_SNAKE
