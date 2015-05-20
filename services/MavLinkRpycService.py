__author__ = 'luis'
import rpyc
import websocket
from websocket import create_connection
import os,sys
from tornado.options import  options

#path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])
#path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/'))
#sys.path.insert(0, path)
#import serverHCS

class MavLinkRpycService(rpyc.Service):
    #ws = None
    def __init__(self,conn):
        self.ws = None
        #self.ws = websocket.create_connection("ws://127.0.0.1:8888/chatsocket")
        try:
            cmd = "ws://" + options.host + ":" + str(options.port) + "/chatsocket"
            self.ws = websocket.create_connection(cmd)
        except:
            print "No ha sido posible crear la conexioon web para el enviio de paquetes mavlink"
        self.conn = conn # creado para ser utilizado en reconnect
        rpyc.Service.__init__(self,conn)

    def on_connect(self):
        print "Servidor conectado"
        if not self.ws == None:
            websocket.enableTrace(True)
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_get_answer(self): # this is an exposed method
        return 42

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"

    def exposed_imprime(self, datos):
        print datos
        if(datos == "MAV_MODE_FLAG"):
            print "punto de interrupcioon"
        if not self.ws == None:
            self.ws.send(str(datos))

    #def exposed_reconnect(self): #experimental LIM 22/1/15
    #    self.ws = None
    #    #self.ws = websocket.create_connection("ws://127.0.0.1:8888/chatsocket")
    #    self.ws = websocket.create_connection("ws://192.168.1.33:8888/chatsocket")
    #    rpyc.Service.__init__(self,self.conn)