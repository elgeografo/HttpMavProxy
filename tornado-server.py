__author__ = 'Luis Izquierdo Mesa'

import tornado.options
import tornado.web

IP_SERVER = "192.168.1.38"
MAVLINK_SERIAL_PORT = "/dev/tty.usbmodemfd111"
MAVLINK_BAUDIOS = "115200"

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("host", default=IP_SERVER, help="run on the given port")
define("serialPort", default=MAVLINK_SERIAL_PORT, help="Autopilot serial port")
define("baudrate", default=MAVLINK_BAUDIOS, help="Autopilot baud rate")

from services import AutopilotWebManagementService,MavLinkRpycService,MavLinkWebsocketService


class Application(tornado.web.Application):
    def __init__(self):
        self.clientPath = "app"
        handlers = [
            (r"/autopilot", AutopilotWebManagementService.AutopilotWebManagementService ),
            (r"/chatsocket", MavLinkWebsocketService.MavLinkWebsocketService),
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers,**settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port,options.host)
    print "Init server"
