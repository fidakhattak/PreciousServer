import time
import collections
import grovepi
import math
from lxml import etree
from datetime import datetime

class sensor:
    def __init__(self, name, pin, thresholds):
        self.name = name
        self.pin = pin
        self.instantaneous = 0
        self.current = 0
        self.maximum = 0
        self.minimum = 1000
        self.total_samples = 0
        self.sample_size = 10
        self.samples = collections.deque(maxlen = self.sample_size)
        self.total = 0
        self.average_overall = 0
        self.min_threshold = thresholds[0]
        self.max_threshold = thresholds[1]
        self.start_time = time.time() 
        self.last_sample_time = time.time() 
    
    def run_time(self):
            time_passed = self.last_sample_time - self.start_time
            return str(time_passed)

    def update_values(self):
        if self.name == "temperature":
            try:
                temp_var = grovepi.dht(self.pin, 1)
                if type(temp_var) is int:
                    value = "IOError"
                else:
                    value = temp_var[0]
            except IOError: 
                value = "IOError"
        elif self.name == "humidity":
            try:    
                temp_var = grovepi.dht(self.pin, 1)
                if type(temp_var) is int:
                    value = "IOError"
                else:
                    value = temp_var[1]
            except IOError:
                value = "IOError"
        elif self.name == "light":
            grovepi.pinMode(self.pin, "INPUT")
            try:
                value = grovepi.analogRead(self.pin)
            except IOError:
                value = "IOError"
        elif self.name == "air":
            grovepi.pinMode(self.pin, "INPUT")
            try:
                value = grovepi.analogRead(self.pin)
            except IOError:
                value = "IOError"
        else:
            return "invalid sensor: " +self.name
        
        if (value != "IOError"):
            x = float(value)
            if math.isnan(x):
                return "invalid value for " +self.name
            if self.name == "temperature" or self.name == "humidity":
                self.instantaneous = value
                self.samples.appendleft(value)
                l = list(collections.deque(self.samples))
                self.current = sum(l) / float (len(l))
                self.last_sample_time = time.time()
                if self.current > self.maximum: 
                    self.maximum = self.current
                elif self.current < self.minimum: 
                    self.minimum = self.current
                self.total_samples += 1
            elif self.name == "light" or "air":
               self.calibrate_analog(value)         
            s = "Successful update for %s. Current value is %d" %(self.name, self.current)
            return s
        else:
            return "IOError: Could not update %s" %self.name
   
    def calibrate_analog(self,value):
            if self.name =="air":
                value = self.max_threshold - value;
            self.instantaneous = value * 100 / self.max_threshold
            self.samples.appendleft(self.instantaneous)
            l = list(collections.deque(self.samples))
            self.current = sum(l) / float (len(l))
            self.last_sample_time = time.time()
            if self.current > self.maximum: 
                self.maximum = self.current
            elif self.current < self.minimum: 
                self.minimum = self.current
            self.total_samples += 1
   

    def get_values(self):
        element = etree.Element("sensor", sensor_type=self.name)
            
        current_value = etree.Element("Current_Value")
        current_value.text = str(self.current)
        element.append(current_value)
         
        minimum_threshold = etree.Element("Minimum_Threshold")
        minimum_threshold.text = str(self.min_threshold)
        element.append(minimum_threshold)
            
        maximum_threshold = etree.Element("Maximum_Threshold")
        maximum_threshold.text = str(self.max_threshold)
        element.append(maximum_threshold)
        
        sample_time = etree.Element("Sample_Time")
        t = datetime.fromtimestamp(self.last_sample_time)
        sample_time.text = t.strftime("%Y-%m-%d %H:%M:%S")
        element.append(sample_time)

        s = ""    
        s += etree.tostring(element, pretty_print=True)
        return element

if __name__ == "__main__":
    temperature = sensor("temperature", 2, -40, 100) 
    print temperature.current
    print temperature.maximum
    print temperature.minimum
    print temperature.instantaneous
    print temperature.current_time
    print temperature.start_time
    print temperature.total_samples
    print temperature.run_time()

    for x in xrange(1,10):
        print temperature.update_values()
        print "current value => ", temperature.current
        print "maximum_value => ", temperature.maximum
        print "miminum_value => ", temperature.minimum
        print "instantanous value =>", temperature.instantaneous
        print "current_time =>", temperature.current_time
        print "start_time => ", temperature.start_time
        print "total_samples => ", temperature.total_samples
        print temperature.run_time()

   

