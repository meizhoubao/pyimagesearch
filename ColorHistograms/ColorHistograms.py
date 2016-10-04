from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required = True,help = "path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
# cv2.imshow("image",image)
'''
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray",gray)
hist = cv2.calcHist([gray],[0],None,[256],[0,256])
plt.figure()
plt.title("Grayscale HIstogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
plt.plot(hist)
plt.xlim([0,256])
plt.show()
cv2.waitKey(0)
'''
chans = cv2.split(image)
colors = ['b','g','r']
plt.figure()
plt.title("'Flattened' Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of pixels")
features = []

for (chan,color) in zip(chans,colors):
    hist = cv2.calcHist([chan],[0],None,[256],[0,256])
    features.extend(hist)
    plt.plot(hist,color=color)
    plt.xlim([0,256])
plt.show()
print "flattened feature vector size: %d" % (np.array(features).flatten().shape)
