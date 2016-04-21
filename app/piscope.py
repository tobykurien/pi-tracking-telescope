import yaml
import codecs
from modules.camera import Camera
from screens.mainscreen import MainScreen
from ui.ui import UserInterface

def read_config(filepath):
	# read configuration file
	config = {}
	with codecs.open('config.yml', 'r', encoding='utf8') as f:
		yml_dict = yaml.safe_load(f)
		for k in yml_dict:
			config[k] = yml_dict[k]

	return config

if __name__ == "__main__":
	screen = MainScreen()
	ui = UserInterface(screen, (800, 480), True, 60, True)
	config = read_config('config.yml')

	cam = Camera(rpiCam=config['rpi_camera'], cameraNum=config['camera_number'],
					width=config['camera_width'], height=config['camera_height'],
					fps=config['camera_fps'])
		
	while True:
		image = cam.grabFrame()		
		if (image != None): screen.setImage(image)
		ui.tick()
			
	cam.cleanup()	
