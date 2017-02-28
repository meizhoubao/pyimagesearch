from sklearn.cluster import MiniBatchKMeans
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-c", "--clusters", required=True, type=int,
                help="# of clusters")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
(h, w) = image.shape[:2]

image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
image = image.reshape(image.shape[0] * image.shape[1], 3)

clt = MiniBatchKMeans(n_clusters=args["clusters"])
labels = clt.fit_predict(image)
quant = clt.cluster_centers_.astype("uint8")[labels]

quant = quant.reshape((h, w, 3))
image = image.reshape((h, w, 3))

quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)

cv2.imshow("image", np.hstack([image, quant]))
cv2.waitKey(0)
