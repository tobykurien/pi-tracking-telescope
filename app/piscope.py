import cv2
import yaml
import codecs
from modules.camera import Camera
from modules.focus import ProcessFocus
from modules.stacking import ProcessStacking

def read_config(filepath):
	# read configuration file
	config = {}
	with codecs.open('config.yml', 'r', encoding='utf8') as f:
		yml_dict = yaml.safe_load(f)
		for k in yml_dict:
			config[k] = yml_dict[k]

	return config

if __name__ == "__main__":
	config = read_config('config.yml')

	focus = ProcessFocus()
	focus.start()
	
	stack = ProcessStacking()
	stack.start()

	cam = Camera(rpiCam=config['rpi_camera'], cameraNum=config['camera_number'])
	cv2.namedWindow("Image", flags=cv2.CV_WINDOW_AUTOSIZE)
	
	showStack = True
	while True:
		image = cam.grabFrame()		

		# detect focus
		focus.addFrame(image)

		# stack images
		stack.addFrame(image)

		if showStack and stack.outputFrame is not None:
			image = stack.getFrame()
					
		# show the image
		cv2.putText(image, "Focus: {:.2f} Stacking: {}".format(focus.focus, showStack), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
		cv2.imshow("Image", image)
		
		# call waitKey otherwise image won't show. Max 60fps
		key = cv2.waitKey(16) & 0xFF
		if key == 115: 
			# press "s" to toggle stacking 
			showStack = not showStack
			stack.clear()
			
		elif key != 255: break;
	
	cam.cleanup()	
	cv2.destroyAllWindows()
