import cv2
import yaml
import codecs

from modules.camera import Camera

def read_config(filepath):
	# read configuration file
	config = {}
	with codecs.open('config.yml', 'r', encoding='utf8') as f:
		yml_dict = yaml.safe_load(f)
     	for k in yml_dict:
     		config[k] = yml_dict[k]    

	return config

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()
	
if __name__ == "__main__":
	config = read_config('config.yml')
	
	cam = Camera(rpiCam=config['rpi_camera'], cameraNum=config['camera_number'])
	cv2.namedWindow("Image", flags=cv2.CV_WINDOW_AUTOSIZE)
	while True:
		image = cam.grabFrame()
		# detect focus
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		fm = variance_of_laplacian(gray)
		text = "Not Blurry"
		if fm < 100:
			text = "Blurry"
		
		# show the image
		cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
		cv2.imshow("Image", image)	
		
		# call waitKey otherwise image won't show. Max 60fps
		key = cv2.waitKey(16) & 0xFF
		if key != 255: break;
	
	cam.cleanup()	
	cv2.destroyAllWindows()
