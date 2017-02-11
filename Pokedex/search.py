from searcher import Searcher
from zernikemoments import ZernikeMoments
from pyimagesearch import imutils
import numpy as np
import argparse
import cPickle
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-", "--index", required = True,
        help = "Path to where the index file will be stored")
ap.add_argument("-q", "--query", required=True,
        help = "Path to the query image")
args = vars(ap.parse_args())

index = open(args["index"]).read()
index = cPickle.loads(index)

image = cv2.imread(args["query"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = imutils.resize(image, width = 64)

thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 11, 7)

outline = np.zeros(image.shape, dtype="uint8")
(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
cv2.drawContours(outline, [cnts], -1, 255, -1)

desc = ZernikeMoments(21)
queryFeatures = desc.describe(outline)
searcher = Searcher(index)
results = searcher.search(queryFeatures)
print "That pokemon is: %s" % results[0][1].upper()

cv2.imshow("image", image)
cv2.waitKey(0)
