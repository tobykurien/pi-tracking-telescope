# adapted from http://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
import cv2
import sys

sys.path.append("../modules")
from camera import Camera


def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()
	
if __name__ == "__main__":
	cam = Camera(cameraNum=1)
	
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
		cv2.waitKey(0)
