import socket
import sys
import threading
import time

from ConfigParser import SafeConfigParser
from lxml import etree
from grovepi import manager

sensors = ['temperature_sensor', 'humidity_sensor']
config_file = "sensor.config"

DEFAULT_PORT = 5000
DEFAULT_ADDRESS = ''

class server:
    
    def __init__(self):
        self.address = DEFAULT_ADDRESS
        self.port = DEFAULT_PORT
        self.sock = None
        
        self.thread_list = []

    def run(self):
        created = False
        try_count = 0

        while not created:
            if try_count > 3:
                print "Could not create a socket or bind to port"
                print "Try a different port"
                sys.exit(1)
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind((self.address,self.port))
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.sock.listen(5)
                created = True
            except socket.error, err:
                print "socket error, retrying in 5 seconds"
                del self.sock 
                time.sleep(5)
                try_count += 1

        print "Precious Server is online at port " + str(DEFAULT_PORT)
        try:
            while True:
                if threading.active_count() > 5:
                    print "Too many connections"
                    time.sleep(1)
                else:
                    client_socket, client_address = self.sock.accept()
                    new_thread = client(client_socket)
                    print "New incoming connection"
                    print "New thread " + new_thread.getName() + "started"
                    print "Thread active count is" + str(threading.active_count())
                    self.thread_list.append(new_thread)
                    new_thread.start()
        except KeyboardInterrupt:
            print "Clt+C pressed, exiting program"
            self.sock.close()
        except Exception, err:
            print "Exception caught: %s \n Closing .. " %err
        for thread in self.thread_list:
            thread.join(1.0)
        self.sock.close()
        sys.exit(1)


class client(threading.Thread):
    
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.socket = client_socket
    
    def run(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if data:
                    print data
                    print "this was all the data"
                    req = self.parse_data(data)
                    print "function returned"
                    data2= self.create_response(req)
                    print "create_response returned"
                    self.socket.send(data2+"\n")
                    print "socket data sent returned"
                    self.socket.close()
                    return
                else:
                    print "Connection Closed from remote host"
                    self.socket.close()
                    return
            except Exception:
                print "Exception.. Exiting"  
                self.socket.close()
                return
        print "thread " +self.getName() + " terminating"
    
    def parse_data(self, data):
        print "going to format string"
        print data
        root = etree.fromstring(data) 
        print etree.tostring(root)
        req = request()
        for element in root.iter():
            if element.tag == "sensors_value":
                req.command = "sensors_value"
                req.valid = True
            elif element.tag == "sensor_type":
                req.sensor += element.text
            elif element.tag == "value_type":
                req.value = element.text
            else:
                print "non a valid request"
                return -1
            print "element.tag", element.tag
            print "element.text", element.text
        return req

    def create_response(self, req):
        print "create_response started"
        print req
        if not req.valid:
            return "Error: Wrong Request"
        print "calling manage.get_responce"
        return manage.get_response(req)

class request:
    def __init__(self):
        self.valid = False
        self.command = ""
        self.sensor = ""
        self.value = ""

if "__main__" == __name__ :
    manage = manager.manager()
    server = server()
    server.run()
    print "terminated" 
