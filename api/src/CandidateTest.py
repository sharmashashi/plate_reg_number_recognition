import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks_cwt


class CandidateTest:

    # compare reversed and normal y coordinate, if normal is higher increase it to max height to
    # identify that it is our peak. If normal is lower make it 0
    def better_peak_data(self, normal, reverse, x, height):
        y = []

        i = 0
        while i < len(normal):
            ytemp = normal[i]
            if normal[i] > reverse[i]:
                ytemp = height
            else:
                ytemp = 0
            y.append(ytemp)
            i = i+1

        # plt.plot(x, y)
        # plt.show()

        no_of_intersection = 0
        i = 0
        while i < len(y):
            st = False
            nd = False
            if i > 0 and y[i-1] == 0 and y[i] == height:
                st = True
            if i > 0 and y[i-1] == height and y[i] == 0:
                nd = True

            if st == True or nd == True:
                no_of_intersection = no_of_intersection+1
            i = i+1

        return no_of_intersection
    # row and column profiling to make sure candidate is license number plate

    def profile_test(self, candidate_image_path):
        candidate_image = cv2.resize(cv2.imread(
            candidate_image_path, cv2.IMREAD_UNCHANGED), (400, 300))
        rows, columns = candidate_image.shape
        height = rows
        width = columns
        x_avg_normal = []
        x_avg_reverse = []
        y_col = []
        # row sum
        for i in range(rows):
            y_col.append(i)
            # print(binary_image[i][5])
            sum = 0
            for j in range(columns):
                sum = sum + candidate_image[i][j]
            x_avg_normal.append(sum/height)
            x_avg_reverse.append(((height/2)-(sum/height)))
        # plt.plot(y_col, x_avg_normal)
        # plt.plot(y_col, x_avg_reverse)
        # plt.show()

        vertical_cut = self.better_peak_data(
            x_avg_normal, x_avg_reverse, y_col, height)

        y1_avg_normal = []
        y1_avg_reverse = []
        x1_col = []
        # column sum
        for i in range(columns):
            x1_col.append(i)
            # print(binary_image[i][5])
            sum = 0
            for j in range(rows):
                sum = sum + candidate_image[j][i]
            y1_avg_normal.append(sum/height)
            y1_avg_reverse.append((height/2)-sum/height)

        # plt.plot(x1_col, y1_avg_normal)
        # plt.plot(x1_col, y1_avg_reverse)
        # plt.show()
        horizontal_cut = self.better_peak_data(
            y1_avg_normal, y1_avg_reverse, x1_col, height)

        # to identify a number plate, there should be at least 4 (2*2) vertical cut
        # and 8 (4*2) horizontal cut
        plate_located = False
        if vertical_cut >= 4 and horizontal_cut >= 8:
            plate_located = True

        return plate_located

        # or this
        # sumOfColumns = np.sum(candidate_image, axis=0)
        # sumOfRows = np.sum(candidate_image, axis=1)
        # plt.plot(sumOfRows)
        # plt.show()
        # plt.plot(sumOfColumns)
        # plt.show()

    def aspect_ratio_test(self, ratio):
        rear_lower = 5/3.5
        rear_upper = 5/2.5
        val = False
        if ratio > rear_lower and ratio < rear_upper or ratio < 4.5 or ratio > 3.5:
            val = True
        return val
