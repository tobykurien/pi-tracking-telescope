import cv2
import yaml
import codecs
from modules.camera import Camera
from modules.focus import ProcessFocus

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
	
	cam = Camera(rpiCam=config['rpi_camera'], cameraNum=config['camera_number'])
	cv2.namedWindow("Image", flags=cv2.CV_WINDOW_AUTOSIZE)
	while True:
		image = cam.grabFrame()		

		# detect focus
		if focus.queue.qsize() == 0:
			focus.queue.put(image)
			
		text = "Not Blurry"
		if focus.focus < 100:
			text = "Blurry"
		
		# show the image
		cv2.putText(image, "{}: {:.2f}".format(text, focus.focus), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
		cv2.imshow("Image", image)	
		
		# call waitKey otherwise image won't show. Max 60fps
		key = cv2.waitKey(16) & 0xFF
		if key != 255: break;
	
	cam.cleanup()	
	cv2.destroyAllWindows()
