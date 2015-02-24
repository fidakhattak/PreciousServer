import collections 

class test:
    
    def __init__(self):
        window_size = 10
        self.averaging_window = collections.deque(maxlen = window_size)
    
    def test_queue(self):
        string = "Hello Pakistan, How is the weather today"
        l = list(string)
        i = 0
        while i < len(l):
            print l[i]
            self.averaging_window.appendleft(l[i])
            l2 = list(self.averaging_window)
            print l2
            i += 1

element = test()
element.test_queue()
