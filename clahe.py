from matplotlib import pyplot as plt
import numpy as np
import argparse
import glob
import sys
import cv2
import os

cwd = os.getcwd()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])

# """""""""""""""""""""""""""""""Flattened color histogram"""""""""""""""""""""""
# grab the image channels, initialize the tuple of colors,
# the figure and the flattened feature vector
chans = cv2.split(image)
colors = ("b", "g", "r")
plt.figure()
plt.title("Flattened Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
features = []

for (chan, color) in zip(chans, colors):
    # create a histogram for the current channel and
	# concatenate the resulting histograms for each
	# channel
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    features.extend(hist)
    plt.plot(hist, color = color)
    plt.xlim([0, 256])

############################CLAHE histogram equalization###########################
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(gray)

equalized_image = cv2.cvtColor(cl1, cv2.COLOR_GRAY2BGR)

chans = cv2.split(equalized_image)
plt.figure()
plt.title("CLAHE-processed Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
features = []

for (chan, color) in zip(chans, colors):
    # create a histogram for the current channel and
	# concatenate the resulting histograms for each channel
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    features.extend(hist)
    plt.plot(hist, color = color)
    plt.xlim([0, 256])

plt.show()

cv2.imshow("image", image)
cv2.imshow("equalized image", equalized_image)

if cv2.waitKey(0):
    cv2.destroyAllWindows()