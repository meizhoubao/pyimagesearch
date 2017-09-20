import numpy as np
import argparse
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-p", "--prototxt", required=True, help="Path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="Path to Caffe pre-trained model")
ap.add_argument("-l", "--labels", required=True, help="Path to ImageNet labels (i.e., syn-sets)")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
rows = open(args["labels"]).read().strip().split("\n")
classes = [r[r.find(" ") + 1:].split(",")[0] for r in rows]

blob = cv2.dnn.blobFromImage(image, 1, (224, 224), (104, 117, 123))

print("[INFO] loding model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
net.setInput(blob)
start = time.time()
preds = net.forward()
end = time.time()
print("[INFO] classification took {:.5} seconds".format(end-start))
idxs = np.argsort(preds[0])[::-1][:5]

for (i, idx) in enumerate(idxs):
    if i == 0:
        text = "label: {}, {:.2f}%".format(classes[idx], preds[0][idx] * 100)
        cv2.putText(image, text, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    print("[INFO] {}. label: {}, probability: {:.5}".format(i+1, classes[idx], preds[0][idx]))

cv2.imshow("Image", image)
cv2.waitKey(0)
