import cv2
from skimage import feature

class FeatureExtractor:
    @staticmethod
    def hog_feature_extractor(char_image_path):
        IMAGE = cv2.imread(char_image_path)
        hog, hog_image = feature.hog(IMAGE, orientations=9, pixels_per_cell=(
            8, 8), cells_per_block=(2, 2), block_norm='L2-Hys', visualize=True, transform_sqrt=True)
        return hog
