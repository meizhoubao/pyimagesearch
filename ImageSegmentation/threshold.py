import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be thresholded")
ap.add_argument("-t", "--threshold", type=int, default=128,
                help="Threshold value")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

methods = [
    ("THRESH_BINARY", cv2.THRESH_BINARY),
    ("THRESH_BINARY_INV", cv2.THRESH_BINARY_INV),
    ("THRESH_TRUNC", cv2.THRESH_TRUNC),
    ("THRESH_TOZERO", cv2.THRESH_TOZERO),
    ("THRESH_TOZERO_INV", cv2.THRESH_TOZERO_INV),
]

for (threshName, threshMethod) in methods:
    (T, thresh) = cv2.threshold(gray, args["threshold"], 255, threshMethod)
    cv2.imshow(threshName, thresh)
    cv2.waitKey(0)
