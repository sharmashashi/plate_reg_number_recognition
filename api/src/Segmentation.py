import cv2
import numpy as np
import Localization as loc
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

    def prepare_image(self, image):
        # image = cv2.blur(image,(5,5))
        image[...,2]= image[...,2]*.5
        image[...,1]= image[...,1]*1.2
        
        image = cv2.bilateralFilter(image,20,90,90)
        self.showImage("lfksj",image)

        b_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, bin_image = cv2.threshold(b_image, 140, 255, cv2.THRESH_BINARY)
        self.showImage("flsdkj",bin_image)
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

        for each in os.listdir("segmented_images"):
            os.remove("segmented_images/"+each)
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
                cv2.imwrite('segmented_images/'+str(x)+'_'+str(y)+'.png',
                            cropped_image)
                i = i+1
        return divider_ycoordinate
