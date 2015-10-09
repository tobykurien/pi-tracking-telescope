# adapted from http://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/

# import the necessary packages
import cv2
import time


def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

# initialize the camera and grab a reference to the raw camera capture
rawCapture = cv2.VideoCapture(1)

# allow the camera to warmup
time.sleep(0.1)
ret, image = rawCapture.read()

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
key = cv2.waitKey(0)

rawCapture.release()
cv2.destroyAllWindows()