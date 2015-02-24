import threading
from sensor import sensor
import time
from lxml import etree

class manager(threading.Thread):
    sensors_list = ['temperature', 'humidity', 'light', 'air']
    sensors_pins = [4, 4, 0, 1]
    sensors_thresholds =[[-40, 70], [0, 100], [0,1024], [0,1024]]
    sensors = []
    update_interval = 5
    location = "coffee_room"

    def  __init__(self):
        threading.Thread.__init__(self)
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        for i in range(len(self.sensors_list)):
           self.sensors.append (sensor(self.sensors_list[i], self.sensors_pins[i], self.sensors_thresholds[i]))
        thread.start()


    def run(self):
        while True:
            print "daemon thread"
            self.update_sensors()
            time.sleep(self.update_interval)

    def update_sensors(self):
        for i in range(len(self.sensors)):
           print self.sensors[i].update_values()
    
    def get_value(self,sensor_type):
            if sensor_type == "all":
                root = etree.Element("node", location = self.location) 
                s = ""
                print "manager.get_value started: sensor_type = all"
                for i in range(len(self.sensors)):
                    print i
                    print self.sensors[i]
                    print etree.tostring(self.sensors[i].get_values())
                    element= self.sensors[i].get_values()
                    root.append(element)
                return root
            elements = filter(lambda x: x.name == sensor_type, self.sensors)
            if len(elements) > 0:
                return elements[0].get_values()
            else:
                s = "sensor not found"
                return s

    
    def get_response(self, req):
        print "get_response started"
        print req
        if req.command == "sensors_list":
            print "req.command == sensor_list"
            s = "200 OK \n <sensor_list> " +sensors_list + " </sensors_list>"
            root = etree.Element("node", location = self.location) 
            element = etree.Element("sensor_list")
            element.text = str(self.sensor_list)
            root.append(element)
            s = etree.tostring(root)
            print s
            return s
        elif req.command == "sensors_value":
            print "req.command == sensor_value : sensor_type=",req.sensor
            root = self.get_value(req.sensor)
            print etree.tostring(root, pretty_print=True)
            return etree.tostring(root)


if __name__ == "__main__":
    element = manager()
 #   element.update_sensors()
    for x in xrange(1,10):
        s1 = element.get_value("temperature")
        s2 = element.get_value("humidity")
        s3 = element.get_value("Foo")
        doc = etree.XML(s1.strip())
        temperature = doc.findtext("Current_Value")
        print temperature
        root = etree.fromstring(s1)
        print "root.tag is ", root.tag
        print "root.text is ", root.text
        print "etree.tostring(root) is ", etree.tostring(root)

        time.sleep(5)
