from sklearn import svm
from Localization import Localization
from CandidateTest import CandidateTest
from Segmentation import Segmentation
from Sorting import Sorting
import numpy as np
import os
import cv2
import svm_classification.classification as clf


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def segment_and_sort(finalpath):
    seg = Segmentation()
    separator_ycoordinate = seg.segmentation("candidate_image/plate.png")
    sort = Sorting()
    segmented_dir = sort.sort(
        "segmented_images", separator_ycoordinate, finalpath=finalpath)


def start():
    _localization = Localization()
    # gets preprocessed image path
    cropped_image_dir = _localization.localize("source_image.jpg")

    _candidateTest = CandidateTest()
    # remove images from candidate dir
    for each in os.listdir("candidate_image"):
        os.remove("candidate_image/"+each)

    # do iterative profile test and choose  one image for candidate
    for image_name in os.listdir(cropped_image_dir):
        is_candidate = _candidateTest.profile_test(
            cropped_image_dir+image_name)
        if is_candidate:
            image = cv2.imread(cropped_image_dir+image_name)
            cv2.imwrite("candidate_image/"+"plate.png", image)

    segment_and_sort(finalpath="MERGED/merged/")

    #
    #
    reg_number = clf.start_prediction()
    return reg_number


if __name__ == "__main__":
    print(start())
