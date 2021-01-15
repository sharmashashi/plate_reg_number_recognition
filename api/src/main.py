from sklearn import svm
from .Localization import Localization
from .CandidateTest import CandidateTest
from .Segmentation import Segmentation
from .Sorting import Sorting
import numpy as np
import os
import cv2
import api.src.svm_classification.classification as clf


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def segment_and_sort(finalpath):
    seg = Segmentation()
    separator_ycoordinate = seg.segmentation("api/src/candidate_image/plate.png")
    sort = Sorting()
    segmented_dir = sort.sort(
        "api/src/segmented_images", separator_ycoordinate, finalpath=finalpath)


def start():
    _localization = Localization()
    # gets preprocessed image path
    cropped_image_dir = _localization.localize("source_image.jpg")
    
    _candidateTest = CandidateTest()
    # remove images from candidate dir
    for each in os.listdir("api/src/candidate_image"):
        os.remove("api/src/candidate_image/"+each)

    # do iterative profile test and choose  one image for candidate
    for image_name in os.listdir(cropped_image_dir):

        is_candidate = _candidateTest.profile_test(
            cropped_image_dir+image_name)
        if is_candidate:
            image = cv2.imread(cropped_image_dir+image_name)
            cv2.imwrite("api/src/candidate_image/"+"plate.png", image)

    # cv2.imshow("original",
    #     cv2.imread("candidate_image/plate.png"))

    # i = 0
    # while i < 5:
    #     rotated = rotate_image(
    #         cv2.imread("api/src/candidate_image/plate.png"), 7)
    #     cv2.imwrite("api/src/candidate_image/plate.png", rotated)
    #     segment_and_sort(finalpath="api/src/MERGED/merged+"+str(i)+"/")

    #     i += 1

    cv2.imwrite("api/src/candidate_image/plate.png", rotate_image(
        cv2.imread("api/src/candidate_image/plate.png"), 0))
    segment_and_sort(finalpath="api/src/MERGED/merged/")

    # i = 0
    # while i < 5:
    #     rotated = rotate_image(
    #         cv2.imread("api/src/candidate_image/plate.png"), -7)
    #     cv2.imwrite("api/src/candidate_image/plate.png", rotated)
    #     segment_and_sort(finalpath="api/src/MERGED/merged-"+str(i)+"/")
    #     i += 1
        # cv2.imshow("rotated", rotated)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    # cv2.imwrite("api/src/candidate_image/plate.png", rotate_image(
    #     cv2.imread("api/src/candidate_image/plate.png"), +35))
    

    #
    #
    reg_number=clf.start_prediction()
    return reg_number
    