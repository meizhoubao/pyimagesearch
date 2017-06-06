import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

# image = mpimg.imread("chelsea-the-cat.png")
image = cv2.imread("chelsea-the-cat.png")

plt.axis("off")

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()
