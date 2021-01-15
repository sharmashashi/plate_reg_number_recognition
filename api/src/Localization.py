import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from .CandidateTest import CandidateTest


class Localization:
    # provide window name to fix the window size
    def showImage(self, windowName, image):
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(windowName, 600, 600)

        cv2.imshow(windowName, image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def sharpenImage(self, image):
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        sharpened = cv2.filter2D(image, -1, kernel)
        return sharpened

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
        if width is None and height is None:
            return image

    # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

    # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

    # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
        return resized

    def localize(self, imagePath):
        # imreads always takes image in rgb color format
        bgr_image = self.image_resize(cv2.imread(
            imagePath), width=1200)
        # first convert the format to hsv(Hue saturation and value)
        hsvImage = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        # self.showImage("hsv",hsvImage)
        # lower starting color bound for red in hsv spectrum
        lower_red1 = np.array([0, 100, 100])
        # upper bound for red in hsv spectrum
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])

        mask1 = cv2.inRange(hsvImage, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsvImage, lower_red2, upper_red2)
        mask = cv2.bitwise_xor(mask1, mask2)
        masked_image = cv2.bitwise_and(bgr_image, bgr_image, mask=mask)
        # gives masked image that only shows red area
        # self.showImage("masked Image", masked_image)

        # convert to binary image before finding contours
        ret, binary_image = cv2.threshold(
            masked_image, 0, 255, cv2.THRESH_BINARY)
        # self.showImage("binary image",binary_image)

        # edge detection

        # canny edge detection
        canny_edge = cv2.Canny(binary_image, 127, 255)
        # self.showImage("canny edge",canny_edge)

        # find contours
        contours, hir = cv2.findContours(
            canny_edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_image = np.zeros_like(bgr_image)
        # print(contours)
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
        # self.showImage("contours", contour_image)
        _candidateTest = CandidateTest()

        for each in os.listdir("api/src/cropped_images"):
            os.remove("api/src/cropped_images/"+each)
        i = 1
        for cntr in contours:
            x, y, w, h = cv2.boundingRect(cntr)
            ratio = w/h
            # select rectangles only. Works on images with numberplates laid out horizontally
            if w > 80 and h > 50:
                cropped_image = bgr_image[y:y+h, x:x+w]
                # convert it to gray image for feature analysis
                b_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                ret, bin_image = cv2.threshold(
                    b_image, 150, 255, cv2.THRESH_BINARY)
                cv2.imwrite('api/src/cropped_images/image_'+str(i)+'.png',
                            bin_image)
                i = i+1
        return "api/src/cropped_images/"
