"""
    Contrast limiting adaptive histogram equalization.
    Takes in a directory of images and applies CLAHE image processing to
    improve image contrast.

    Unlike adaptive histogram equalization, CLAHE does not overproduce noise in
    homogeneous area.
"""
from matplotlib import pyplot as plt
import scipy.misc
import argparse
import glob
import cv2
import os
import matplotlib
import piexif
from PIL import Image

cwd = os.getcwd()
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True, help = "Directory with the images")
args = vars(ap.parse_args())
images = args["dataset"] + "/"

final_img_dir = cwd + "/" + "CLAHE_results/" + images
histogram_dir = cwd + "/" + "CLAHE_histogram/" + images

if not os.path.exists(final_img_dir):
    os.makedirs(final_img_dir)

if not os.path.exists(histogram_dir):
    os.makedirs(histogram_dir)

if len(final_img_dir) != 0:
    files = glob.glob(final_img_dir + "*")
    for f in files:
        os.remove(f)

if len(histogram_dir) != 0:
    files = glob.glob(histogram_dir + "*")
    for f in files:
        os.remove(f)

cliplimits = [10]

"""
        draws out the color histogram on supplied subplot
        accepts a color channel and a Matplotlib subplot
"""
def drawHist(channels, plt):
    colors = ("b", "g", "r")

    for (chan, color) in zip(channels, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        features.extend(hist)
        plt.plot(hist, color = color)

for img in os.listdir(os.path.abspath(images)):

    #for macs...
    if ".DS_Store" in img:
        continue

    #store EXIF data as bytes, as image conversions strip them away
    exif_dict = piexif.load(cwd + "/" + images + img)
    exif_bytes = piexif.dump(exif_dict)
    image = cv2.imread(cwd + "/" + images + img)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)

    for clip_lim in cliplimits:

        #-----Applying CLAHE to L-channel-------------------------------------------
        clahe = cv2.createCLAHE(clipLimit=clip_lim, tileGridSize=(8,8))
        cl = clahe.apply(l)

        #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
        limg = cv2.merge((cl,a,b))

        #-----Converting image from LAB Color model to RGB model--------------------
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        result_dir = os.path.splitext(final_img_dir + img)[0] + "_clim_" + str(clip_lim) + ".JPEG"
        scipy.misc.imsave(result_dir, final)

        im = Image.open(result_dir)
        im = im.convert('RGB')
        im.save(result_dir, "JPEG", exif=exif_bytes)

        fig = plt.figure()
        plt.title("Clip limit: " + str(clip_lim))

        # ------------------Display the histogram---------------------------
        image_chans = cv2.split(image)
        features = []
        ax1 = fig.add_subplot(1, 2, 1)
        drawHist(image_chans, ax1)

        final_chans = cv2.split(final)
        features = []
        ax2= fig.add_subplot(1, 2, 2)
        drawHist(final_chans, ax2)

        fig.savefig(histogram_dir + img + "clim_" + str(clip_lim) + ".png")

        plt.close()

plt.show()