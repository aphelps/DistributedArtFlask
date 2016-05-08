from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Optional

from wtforms.fields.html5 import DecimalRangeField

from wtforms_components import ColorField

from colour import Color


class RGBForm(Form):
    DEFAULT_RED = 0
    DEFAULT_GREEN = 0
    DEFAULT_BLUE = 0
    DEFAULT_COLOR = Color(rgb=(DEFAULT_RED, DEFAULT_GREEN, DEFAULT_BLUE))

    # red = IntegerField("Red", default=DEFAULT_RED, validators=[Optional()])
    # green = IntegerField("Green", default=DEFAULT_GREEN, validators=[Optional()])
    # blue = IntegerField("Blue", default=DEFAULT_BLUE, validators=[Optional()])
    red = DecimalRangeField('Red', default=DEFAULT_RED)
    green = DecimalRangeField('Green', default=DEFAULT_GREEN)
    blue = DecimalRangeField('Blue', default=DEFAULT_BLUE)
    # color = ColorField("Color")
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        DEFAULT_RED = kwargs.get('red', 0)
        DEFAULT_GREEN = kwargs.get('green', 0)
        DEFAULT_BLUE = kwargs.get('blue', 0)
        # DEFAULT_COLOR = Color(rgb=(DEFAULT_RED, DEFAULT_GREEN, DEFAULT_BLUE))
        print("RGBForm: color:%s,%s,%s" % (DEFAULT_RED, DEFAULT_GREEN, DEFAULT_BLUE))


class SnakeForm(Form):
    DEFAULT_RED = 0
    DEFAULT_GREEN = 0
    DEFAULT_BLUE = 0
    DEFAULT_PERIOD = 100
    DEFAULT_MODE = 0

    red = DecimalRangeField('Red', default=DEFAULT_RED)
    green = DecimalRangeField('Green', default=DEFAULT_GREEN)
    blue = DecimalRangeField('Blue', default=DEFAULT_BLUE)
    period = DecimalRangeField('Period (ms)', default=DEFAULT_PERIOD)
    colormode = DecimalRangeField('Colormode', default=DEFAULT_MODE)

    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        DEFAULT_RED = kwargs.get('red', 0)
        DEFAULT_GREEN = kwargs.get('green', 0)
        DEFAULT_BLUE = kwargs.get('blue', 0)
        DEFAULT_PERIOD = kwargs.get('period', 100)
        DEFAULT_MODE = kwargs.get('colormode', 0)
        print("SnakeForm: bgcolor:%s,%s,%s period:%s mode:%s" %
              (DEFAULT_RED, DEFAULT_GREEN, DEFAULT_BLUE, DEFAULT_PERIOD, DEFAULT_MODE))
