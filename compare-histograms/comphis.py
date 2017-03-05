from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
                help="Path to the directory of images")
args = vars(ap.parse_args())

index = {}
images = {}

for imagePath im glob.glob(args["dataset"] + "/*.png"):
    filename = imagePath[imagePath.rfind("/") + 1:]
    image = cv2.imread(imagePath)
    images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist).flatten()
    index[filename] = hist

# METHOD 1
OPENCV_METHODS = (("Correlation", cv2.cv.CV_COMP_CORREL),
                  ("Chi-Squared", cv2.cv.CV_COMP_CHISQR),
                  ("Intersection", cv2.cv.CV_COMP_INTERSECT),
                  ("Hellinger", cv2.cv.CV_COMP_BHATTACHARYYA))

for (methodName, method) in OPENCV_METHODS:
    results = {}
    reverse = False
    if methodName in ("Correlation", "Intersection"):
        reverse = True
    for (k, hist) in index.items():
        d = cv2.compareHist(index["doge.png"], hist, method)
        results[k] = d
    results = sorted([(v, k) for (k, v) in results.items()], reverse=reverse)

    fig = plt.figure("Query")
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(images["doge.png"])
    plt.axis("off")

    fig = (i, (v, k)) in enumerate(results):
        ax = fig.add_subplot(1, len(images), i + 1)
        ax.set_title("%s: %.2f" % (k, v))
        plt.imshow(images[k])
        plt.axis("off")

plt.show()

# METHOD 2
SCIPY_METHODS = (("Euclidean", dist.euclidean),
                 ("Manhanttan", dist.cityblock),
                 ("Chebysev", dist.chebyshev))

for (methodName, method) in SCIPY_METHODS:
    results = {}
    for (k, hist) in index.items():
        d = method(index["doge.png"], hist)
        results[k] = d
    results = sorted([(v, k) for (k, v) in results.items()])

    fig = plt.figure("Query")
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(images["doge.png"])
    plt.axis("off")

    fig = plt.figure("Results: %s" (methodName))
    fig.subtitle(methodName, fontsize=20)
    for (i, (v, k)) in enumerate(results):
        ax = fig.add_subplot(1, len(images), i+1)
        ax.set_title("%s: %.2f" % (k, v))
        plt.imshow(image[k])
        plt.axis("off")

plt.show()

# METHOD 3


def chi2_distance(histA, histB, eps=1e-10):
    d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])
    return d

# initialize the results dictionary
results = {}

# loop over the index
for (k, hist) in index.items():
    d = chi2_distance(index["doge.png"], hist)
    results[k] = d

# sort the results
results = sorted([(v, k) for (k, v) in results.items()])

# show the query image
fig = plt.figure("Query")
ax = fig.add_subplot(1, 1, 1)
ax.imshow(images["doge.png"])
plt.axis("off")

# initialize the results figure
fig = plt.figure("Results: Custom Chi-Squared")
fig.suptitle("Custom Chi-Squared", fontsize=20)

# loop over the results
for (i, (v, k)) in enumerate(results):
    ax = fig.add_subplot(1, len(images), i + 1)
    ax.set_title("%s: %.2f" % (k, v))
    plt.imshow(images[k])
    plt.axis("off")
# show the custom method
plt.show()
