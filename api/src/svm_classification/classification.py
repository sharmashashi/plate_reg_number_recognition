
# this is main file for svm classification
# run this file directly
# TODO merge after completing preprocessing

import os
import matplotlib.pyplot as plt
import numpy as np
from svm_classification. FeatureExtractor import FeatureExtractor
from svm_classification.Classifier import Classifier
FEATURELABELDIR = "svm_classification/Calculated Feature and Label/"

# calculates feature vector and saves as file along with
# label for each character


def save_feature():
    merged_feature_vector = []
    merged_label = []
    for each_character in os.listdir("train"):
        feature_matrix = []
        feature_label = []
        each_character_dir = "svm_classification/train/"+each_character
        for char_image in os.listdir(each_character_dir):
            char_image_path = each_character_dir+"/"+char_image
            vec = FeatureExtractor.hog_feature_extractor(char_image_path)
            feature_matrix.append(vec)
            feature_label.append(each_character)

        # merge all feature vectors to form a single vector
        # similarly merge label too
        # keep in mind that adjust order of label while merging wrt order of feature vector when merged
        merged_feature_vector.extend(feature_matrix)
        merged_label.extend(feature_label)
    np.save(FEATURELABELDIR +
            "training_feature_matrix.npy", merged_feature_vector)
    np.save(FEATURELABELDIR+"labels.npy", merged_label)


def start_prediction():
    # call this method exactly once
    # no need to call because feature and label will be saved locally
    # save_feature()

    # get saved feature matrix and label vec
    # feature_mat = np.load(FEATURELABELDIR+"training_feature_matrix.npy")
    # label_vec = np.load(FEATURELABELDIR+"labels.npy")
    clf = Classifier()

    # call this method exactly once
    # trained model will be saved in dir and no need to train
    # again
    # clf.train(feature_mat, label_vec)

    # # get test images
    test_image_feature_matrix = []
    test_dir = "MERGED/merged/"
    charactercounts = 0
    for each in os.listdir(test_dir):
        charactercounts += 1
    i = 0
    while i < charactercounts:
        test_image_feature_matrix.append(
            FeatureExtractor.hog_feature_extractor(test_dir+str(i)+".png"))
        i += 1

    characters = ""
    for each in test_image_feature_matrix:
       predictedcharacter= clf.predict(each)
       characters=characters+predictedcharacter+" "
    return characters
