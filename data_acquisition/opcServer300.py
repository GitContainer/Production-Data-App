import snap7.client as c
from snap7.util import *
from snap7.snap7types import *

plc = c.Client()
plc.connect('192.168.10.1', 0, 2)
print(plc.get_connected())
print(plc.as_ct_read())
plc.disconnect()
