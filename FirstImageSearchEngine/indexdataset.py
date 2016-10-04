from rgbhistogram import RGBHistogram
import argparse
import cPickle
import glob
import cv2

ap =argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
        help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True,
        help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

index = {}

desc = RGBHistogram([8,8,8])
for imagePath in glob.glob(args["dataset"] + "/*.png"):
    k = imagePath[imagePath.rfind("/") + 1:]

    image = cv2.imread(imagePath)
    features = desc.describe(image)
    index[k] = features

f = open(args["index"], "w")
f.write(cPickle.dumps(index))
f.close()
