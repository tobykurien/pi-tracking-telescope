class Telescope:
    MAX_SPEED = 10000
    
    def __init__(self, device='/dev/ttyACM0'):
        self.file = open(device, "w")
        
    def setAlt(self, speed):
        if (speed < 0):
            command = 'j'
            val = Telescope.MAX_SPEED + speed
        else:
            command = 'u'
            val = Telescope.MAX_SPEED - speed
            
        if val < 0: val = 0;
        self.file.write("n%sx" % val)
        self.file.write(command)
        self.file.write(command)
        self.file.flush()
    
    def setAzimuth(self, speed):
        if (speed < 0):
            command = 'h'
            val = Telescope.MAX_SPEED + speed
        else:
            command = 'k'
            val = Telescope.MAX_SPEED - speed
            
        if val < 0: val = 0;
        self.file.write("m%sx" % val)
        self.file.write(command)
        self.file.write(command)
        self.file.flush()
    
    def start(self):
        self.file.write("1")
        self.file.flush()
    
    def stop(self):
        self.file.write("0")
        self.file.flush()
