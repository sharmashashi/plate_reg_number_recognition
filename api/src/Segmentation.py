import cv2
import numpy as np
import api.src.Localization as loc
import os


class Segmentation:

    def segmentation(self, image_pat):
        plate_img = cv2.imread(image_pat, cv2.IMREAD_UNCHANGED)
        # kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        # thre_mor = cv2.morphologyEx(plate_img, cv2.MORPH_DILATE, kernel3)
        # lc = loc.Localization
        # lc.showImage("","Contours",plate_img)
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
                b_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                ret, bin_image = cv2.threshold(
                    b_image, 150, 255, cv2.THRESH_BINARY)
                cv2.imwrite('api/src/segmented_images/'+str(x)+'_'+str(y)+'.png',
                            bin_image)
                i = i+1
        return divider_ycoordinate
