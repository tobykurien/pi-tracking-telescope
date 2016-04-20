import cv2
import yaml
import codecs
from modules.camera import Camera
from modules.focus import ProcessFocus
from modules.stacking import ProcessStacking
from datetime import datetime
from screens.mainscreen import MainScreen
from ui import UI

def read_config(filepath):
	# read configuration file
	config = {}
	with codecs.open('config.yml', 'r', encoding='utf8') as f:
		yml_dict = yaml.safe_load(f)
		for k in yml_dict:
			config[k] = yml_dict[k]

	return config

def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
	return datetime.now().strftime(fmt).format(fname=fname)

if __name__ == "__main__":
	screen = MainScreen()
	ui = UI(screen, (800, 480), True, 30, True)
	config = read_config('config.yml')

	# detect focus
	focus = ProcessFocus()
	focus.start()
	
	# stack images
	stack = ProcessStacking()
	stack.start()
	showStack = False

	cam = Camera(rpiCam=config['rpi_camera'], cameraNum=config['camera_number'], 
					width=config['camera_width'], height=config['camera_height'],
					fps=config['camera_fps'])
	#cv2.namedWindow("Image", flags=cv2.CV_WINDOW_AUTOSIZE)
		
	while True:
		image = cam.grabFrame()		

		# do background processing
# 		focus.addFrame(image)
# 		if showStack: stack.addFrame(image)
# 		if showStack and stack.outputFrame is not None:
# 			image = stack.getFrame()

		if (image != None): screen.setImage(image)
		ui.tick()
			
	cam.cleanup()	
	#cv2.destroyAllWindows()
