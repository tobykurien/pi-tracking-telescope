from subprocess import call


class Telescope:
    MAX_SPEED = 10000.0
    MIN_DURATION = 20.0
    MAX_DURATION = 20000.0
    DURATION_CONST=  MAX_SPEED * MIN_DURATION
    
    def __init__(self, device='/dev/ttyACM0'):
        call(("stty -F %s -imaxbel -opost -isig -icanon -echo -echoe -ixoff -ixon 9600" % device).split(" "))

        self.file = open(device, "w")

        
    def setAlt(self, speed):
        if (speed < 0):
            command = 'u'
        else:
            command = 'j'

        duration = self.calcDuration(speed)            
        
        print "n%dx" % duration
        self.file.write("n%dx" % duration)
        self.file.write(command)
        self.file.write(command)
        self.file.flush()

    
    def setAzimuth(self, speed):
        if (speed < 0):
            command = 'k'
        else:
            command = 'h'
        
        duration = self.calcDuration(speed)            
        print "m%dx" % duration
        self.file.write("m%dx" % duration)
        self.file.write(command)
        self.file.write(command)
        self.file.flush()

    def setSteps(self, num):
	self.file.write(num);
	self.file.flush();

    def up(self):
	self.file.write("s");
	self.file.flush();

    def down(self):
	self.file.write("w");
	self.file.flush();

    def left(self):
	self.file.write("d");
	self.file.flush();

    def right(self):
	self.file.write("a");
	self.file.flush();

        
    def calcDuration(self, speed):
        if speed == 0:
            speed = 1
        duration = Telescope.DURATION_CONST / speed
        duration = int(abs(duration))
        if duration > Telescope.MAX_DURATION:
            duration = Telescope.MAX_DURATION
        if duration <= Telescope.MIN_DURATION: 
            duration = Telescope.MIN_DURATION
            
        return duration
            

    
    def start(self):
        self.file.write("1")
        self.file.flush()
    
    def stop(self):
        self.file.write("0")
        self.file.flush()
