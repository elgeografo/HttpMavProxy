# -*- coding: utf-8 -*-
__author__ = 'luis'

import sys
import os.path
import threading
from loginService import UserBaseHandler
import time
from services import MavLinkRpycService
from tornado.options import options
from importlib import import_module
import subprocess
import rpyc



class AutopilotWebManagementService(UserBaseHandler):
    def get(self, *args, **kwargs):
        command = self.get_argument('command')
        awm = AutopilotWebManagement()
        if command=='start':
            awm.startConnection()
            self.write({'result':1})
        if command=='uploadwp':
            awm.uploadWaypoints(self.get_argument('wp'))
            self.write({'result':1})
        if command=='downloadwp':
            awm.downloadWaypoints()
            self.write({'result':1})
        if command=='mavProxyCommand':
            awm.sendMavProxyCommand(self.get_argument('content'))
            self.write({'result':1})
        if command=='kill':
            awm.kill() # kill the rpyc threat of the mavlink and the mavlink
            self.write({'result':1})

        #if command=='stop':
        #    awm.stopConnection()
        #    self.write({'result':2})

class AutopilotWebManagement():
    procMavLinkReader = None
    threadMavLink = None
    c = None
    def __init__(self):
        #self.relativeMapProxyPath = "/MAVProxy-1.3.12/MAVProxy"
        self.relativeMapProxyPath = "/MAVProxy-1.4.4/MAVProxy"
        self.mserial = ""
        self.c = None
    def startConnection(self):
        if AutopilotWebManagement.threadMavLink == None:
            AutopilotWebManagement.threadMavLink = mavLinkServiceThread()
            AutopilotWebManagement.threadMavLink.start()
            path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])
            path = path + self.relativeMapProxyPath
            cmd = "python '" + path + "/mavproxy.py' --master="+ options.serialPort +" --baud=" + options.baudrate + " --logfile='" + path + "/luisLog.log'"
            cmd = cmd + " --out=10.211.55.6:14550"
            AutopilotWebManagement.procMavLinkReader =  subprocess.Popen(cmd , shell = True)
            count = 0
            while (count < 5):
                try:
                    AutopilotWebManagement.c = rpyc.connect("localhost", 18862)
                    count = 5
                except:
                    count = count + 1
                    print "trying to connect. Number of attemps: " + str(count)
                time.sleep(0.5)
            print "rpyc connected"

    def uploadWaypoints(self,file):
        #cmd = "wp save /Volumes/datos1/basura/wpUp37.txt"
        #AutopilotWebManagement.c.root.sendCommand(cmd)
        cmd = "wp load " + file
        AutopilotWebManagement.c.root.sendCommand(cmd)

    def downloadWaypoints(self):
        path = '/'.join(os.path.dirname(__file__).split('/')[:-1])
        path = path + self.relativeMapProxyPath
        #cmd = "python '" + path + "/mavproxy.py' wp save /Volumes/datos1/descargas/filewp.txt"
        #cmd = "wp save /Volumes/datos1/descargas/filewp.txt"
        cmd = "reboot"
        AutopilotWebManagement.c.root.sendCommand(cmd)
        #AutopilotWebManagement.procMavLinkReader =  subprocess.Popen(cmd , shell = True)
        #cmd = "wp save /Volumes/datos1/descargas/filewp.txt"
        #AutopilotWebManagement.procMavLinkReader =  subprocess.Popen(cmd , shell = True)

    def sendMavProxyCommand(self,cmd):
        AutopilotWebManagement.c.root.sendCommand(cmd)

    def kill(self):
        AutopilotWebManagement.c.root.kill()
        if not(AutopilotWebManagement.threadMavLink == None):
            AutopilotWebManagement.threadMavLink.stop()
        #threadWeb.stop()
    #def stopConnection(self):
    #    print "Stoping..."
    #    AutopilotWebManagement.procMavLinkReader.terminate()

class mavLinkServiceThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.t = None

    def run(self):
        from rpyc.utils.server import ThreadedServer
        self.t = ThreadedServer(MavLinkRpycService.MavLinkRpycService, port = 18861)
        #t = ThreadedServer(MyService, port = 18861)
        self.t.start()

    def stop(self):
        if not(self.t==None):
            self.t.exit() # https://docs.python.org/2/library/thread.html

    #def reconnect(self):
    #    c = rpyc.connect("localhost", 18861) #LIM
    #    c.root.reconnect()