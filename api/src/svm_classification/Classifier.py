
from sklearn import svm
import pickle


class Classifier:
    _filename = "trained_model.sav"

    def train(self, feature_mat, label_vec):
        classifier = svm.SVC(gamma=0.001, C=100)
        classifier.fit(feature_mat, label_vec)
        # save trained model
        pickle.dump(classifier, open("api/src/svm_classification/Trained Model/"+self._filename, 'wb'))
        print("model saved")

    def predict(self, input_feature_mat):
        # get saved model
        trained_model = pickle.load(
            open("api/src/svm_classification/Trained Model/"+self._filename, 'rb'))
        predicted = trained_model.predict([input_feature_mat])
        # print("Prediction Successful")
        # print(predicted)
        return predicted[0]
