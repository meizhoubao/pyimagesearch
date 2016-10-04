from rgbhistogram import RGBHistogram
from searcher import Search
import numpy as np
import argparse
import cPickle
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
        help = "Path to the directory that contains the images we just indexed")
ap.add_argument("-i" ,"--index", required = True,
        help = "Path to where we stored our index")
ap.add_argument("-q", "--query", required = True,
        help ="Path to query image")
args = vars(ap.parse_args())

queryImage = cv2.imread(args["query"])
cv2.imshow("Query", queryImage)
print "query: %s" % (args["query"])

desc = RGBHistogram([8,8,8])
queryFeatures = desc.describe(queryImage)

index = cPickle.loads(open(args["index"]).read())
searcher = Search(index)
results = searcher.search(queryFeatures)

montageA = np.zeros((166*5, 400 ,3), dtype = "uint8")
montageB = np.zeros((166*5, 400, 3), dtype = "uint8")

for j in xrange(0, 10):
    (score, imageName) = results[j]
    path = args["dataset"] + "/%s" % (imageName)
    result = cv2.imread(path)
    print "\t%d. %s : %.3f" % (j + 1, imageName, score)

    if j< 5:
        montageA[j*166 : (j+1)*166,:] = result
    else:
        montageB[(j-5)*166 : ((j-5) + 1) * 166, :] = result

cv2.imshow("Results 1-5", montageA)
cv2.imshow("Results 6-10", montageB)
cv2.waitKey(0)
