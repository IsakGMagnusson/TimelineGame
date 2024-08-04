from engineio.payload import Payload
from Sockets.Settings import *
from Sockets.Gameplay import *
from Sockets.Fetch import *
from Sockets.Connect import *

# https://github.com/zauberzeug/nicegui/issues/209
Payload.max_decode_packets = 50

