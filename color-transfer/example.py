from color_transfer import color_transfer
import numpy as np
import argparse
import cv2


def show_image(title, image, width=300):
    r = width / float(image.shape[1])
    dim = (width, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow(title, resized)

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,
                help="Path to the source image")
ap.add_argument("-t", "--target", required=True,
                help="Path to the target image")
ap.add_argument("-o", "--output", help="Path to the output image (optional)")
args = vars(ap.parse_args())

source = cv2.imread(args["source"])
target = cv2.imread(args["target"])

transfer = color_transfer(source, target)

if args["output"] is not None:
    cv2.imwrite(args["ouput"], transfer)

show_image("source", source)
show_image("target", target)
show_image("transfer", transfer)
cv2.waitKey(0)
