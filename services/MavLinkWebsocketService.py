__author__ = 'luis'
import tornado.websocket
import logging

class MavLinkWebsocketService(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        MavLinkWebsocketService.waiters.add(self)
        print "Nuevo  cliente"

    def on_close(self):
        MavLinkWebsocketService.waiters.remove(self)

    @classmethod
    def send_updates(cls, chat):
        #logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)


    def on_message(self, message):
        MavLinkWebsocketService.send_updates(message)