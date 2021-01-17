import cv2
import numpy as np
import api.src.Localization as loc
import os


class Segmentation:

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

    def masking_white(self, image):
        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # lower starting color bound for red in hsv spectrum
        lower_white = np.array([0, 0, 168])
        upper_white = np.array([172, 111, 255])

        mask1 = cv2.inRange(hsvImage, lower_white, upper_white)
        masked_image = cv2.bitwise_and(image, image, mask=mask1)
        return masked_image

    def prepare_image(self, image):
        image = cv2.blur(image, (3, 3))
        b, g, r = cv2.split(image)
        # self.showImage("blue",b)
        # self.showImage("green",g)
        # self.showImage("red",r)
        # image = cv2.fastNlMeansDenoisingColored(image,h=5,hColor=10)
        # image = cv2.blur(image,(3,3))

        mean = cv2.mean(r)[0]
        print(mean)

        # image[...,0] = image[...,0]*1.5

        # image[..., 1] = image[..., 1]*1.1

        # image[..., 2] = image[..., 2]*multiplyfactor2

        image = cv2.bilateralFilter(image, 20, 90, 90)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # self.showImage("lfksj", image)
        ret, bin_image = cv2.threshold(image, mean, 255, cv2.THRESH_BINARY)
        # self.showImage("flsdkj", bin_image)
        return bin_image

    def segmentation(self, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        plate_img = self.prepare_image(image)
        # blurred = cv2.blur(plate_img,(3,3))
        canny_edge = cv2.Canny(plate_img, 127, 255)
        contours, hir = cv2.findContours(
            canny_edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_image = np.zeros_like(plate_img)
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 1)

        for each in os.listdir("api/src/segmented_images"):
            os.remove("api/src/segmented_images/"+each)
        i = 1
        divider_ycoordinate = 0
        for cntr in contours:
            x, y, w, h = cv2.boundingRect(cntr)
            ratio = h/w
            # select rectangles only. Works on images with numberplates laid out horizontally
            if w > 15 and h > 20:
                if i == 1:
                    divider_ycoordinate = y+h
                cropped_image = plate_img[y:y+h, x:x+w]
                if divider_ycoordinate > y+h:
                    divider_ycoordinate = y+h
                # convert it to gray image for feature analysis
                # b_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                # ret, bin_image = cv2.threshold(
                #     b_image, 150, 255, cv2.THRESH_BINARY)
                # print(cv2.contourArea(cntr))
                # self.showImage("dlskfj;slkjf",cropped_image)
                cv2.imwrite('api/src/segmented_images/'+str(x)+'_'+str(y)+'.png',
                            cropped_image)
                i = i+1
        return divider_ycoordinate
