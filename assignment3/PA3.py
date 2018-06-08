"""
Programming Assignment 3
CS 331
Spring 2018
Team:
Brian Wiltse - wiltseb
Garrett Haley - GarrettHaley
"""

from __future__ import division

import string
import unicodedata
from collections import OrderedDict
from math import log10


class NaiveBayesClassifier:
    # Class file names
    PREPROCESSED_TRAIN = 'preprocessed_train.txt'
    PREPROCESSED_TEST = 'preprocessed_test.txt'

    P_POS = 'p_pos'
    P_NEG = 'p_neg'

    def __init__(self, training_file):
        self.training_file = training_file
        self.bag_of_words = self._get_bag_of_words()
        self.train_feature_vec = self._preprocess(self.training_file)
        self.n_train_samples = len(self.train_feature_vec)
        self.model = self.train_classifier()

        self.test_feature_vec = None

    def _preprocess(self, data_file):
        """
        Preprocesses data into a feature vector.
        :param data_file: Path to a file to convert to a feature vector
        :return: A feature vector with the vocabulary in the first row and featurized samples in subsequent rows.
        """
        bag_size = len(self.bag_of_words)
        data = []
        with open(data_file, 'r') as readfile:
            for line in readfile:
                if line:
                    feature_vec = [0] * bag_size
                    review, label = self.get_review_class(line)
                    for word in set(self.get_words(review)):
                        try:
                            # If word isn't in bag of words, just move on.
                            feature_vec[self.bag_of_words.index(word)] = 1
                        except ValueError:
                            continue
                    feature_vec.append(label)
                    data.append(feature_vec)
        return data

    def evaluate(self, test_file):
        """
        Evaluate the accuracy of predictions based on the model trained in
        train_classifier.

        :param test_file: The file containing reviews and their classes.
        File must be parseable by _preprocess
        :return: Accuracy measure (num_correct / num_samples)
        """
        n_positive = len(self.get_positive_train_samples())
        n_negative = len(self.get_negative_train_samples())
        n_train_samples = len(self.train_feature_vec)

        # Obtain the feature vectors for the test set
        self.test_feature_vec = self._preprocess(test_file)
        num_samples = len(self.test_feature_vec)

        # Obtain samples and their classes
        samples = [line[:-1] for line in self.test_feature_vec]
        classes = [line[-1] for line in self.test_feature_vec]

        # Compute probability that each sample belongs to a given class and make guess
        guesses = [0] * num_samples
        for s_num, sample in enumerate(samples):
            prob_pos = log10(n_positive / n_train_samples)
            prob_neg = log10(n_negative / n_train_samples)
            for feat_num, feature in enumerate(sample):
                if feature == 1:
                    prob_pos += log10(self.model[feat_num][self.P_POS])
                    prob_neg += log10(self.model[feat_num][self.P_NEG])
            if prob_pos >= prob_neg:
                guesses[s_num] = 1

        accuracy = sum([int(clss == guess) for clss, guess in zip(classes, guesses)]) / len(guesses)

        return accuracy

    @staticmethod
    def strip_punctuation(line):
        """
        Strip punctuation from a string
        :param line: A string
        :return: A string with all punctuation stripped
        """
        return line.translate(str.maketrans(dict.fromkeys(string.punctuation)))

    @staticmethod
    def get_review_class(line):
        """
        Get the review and the class as separate entities.
        Punctuation is stripped, and label is returned as an int, and any accented characters
        are converted to ascii.
        :param line: String. The review and it's class (separated by '\t')
        :return: A tuple
        """
        line = NaiveBayesClassifier.strip_punctuation(line)
        review, label = line.split('\t')
        label = int(label.strip())

        try:
            review = unicode(review, 'utf-8')
        except NameError:
            pass
        review = unicodedata.normalize('NFD', review)
        review = review.encode('ascii', 'ignore')
        review = str(review.decode('UTF-8'))

        return review, label

    @staticmethod
    def get_words(review):
        """
        Get an array of words, all converted to lower case, stripped of whitespace.
        :param review: String; a single review.
        :return: An array
        """
        return review.lower().strip().split()

    def get_positive_train_samples(self):
        """
        Get samples in training data that are classified as positive
        """
        return [sample for sample in self.train_feature_vec if sample[-1] == 1]

    def get_negative_train_samples(self):
        """
        Get samples in training data that are classified as negative
        """
        return [sample for sample in self.train_feature_vec if sample[-1] == 0]

    def train_classifier(self):
        """
        Train the Naive Bayes Classifier.
        :return: An ordered dictionary containing the feature vectors
        """
        if not self.train_feature_vec:
            print("Error: must preprocess data first")
            return

        positive_samples = self.get_positive_train_samples()
        n_positive = len(positive_samples)

        # Add up the occurrences of each word over all positive reviews.
        # Each row is a sample; zip(*...) accesses each column
        # Strip off the last element (class label)
        pos_summed_list = [sum(x) for x in zip(*positive_samples)][:-1]

        # Probability of each word, given positive review
        pos_prob_list = [(x + 1) / (n_positive + 2) for x in pos_summed_list]

        # Repeat above steps for negative reviews
        negative_samples = self.get_negative_train_samples()
        n_negative = len(negative_samples)
        neg_summed_list = [sum(x) for x in zip(*negative_samples)][:-1]
        neg_prob_list = [(x + 1) / (n_negative + 2) for x in neg_summed_list]

        # Map each word to its probability, given positive review
        # idx is the index of the word in the sorted bag of words
        return OrderedDict({idx: {self.P_POS: p_pos, self.P_NEG: p_neg}
                            for idx, (p_pos, p_neg) in enumerate(zip(pos_prob_list, neg_prob_list))})

    def _get_bag_of_words(self):
        """
        Set the bag of words for this classifier.
        :return: a sorted set of words that represent all words in the training set
        """
        bow = set()
        with open(self.training_file, 'r') as txtfile:
            for line in txtfile:
                if line:
                    review, _ = self.get_review_class(line)
                    bow.update(self.get_words(review))
        return sorted(bow)


def main():
    training_file = 'trainingSet.txt'
    test_file = 'testSet.txt'
    classifier = NaiveBayesClassifier(training_file)

    with open('results.txt', 'w') as outfile:
        t_f = training_file
        outfile.write("Results of classifying with Naive Bayes Classifier:\n" \
                      "Training data: {}\n" \
                      "Testing data: {}\n" \
                      "Accuracy: {}\n\n".format(training_file, t_f, classifier.evaluate(t_f)))

        t_f = test_file
        outfile.write("Results of classifying with Naive Bayes Classifier:\n" \
                      "Training data: {}\n" \
                      "Testing data: {}\n" \
                      "Accuracy: {}\n".format(training_file, t_f, classifier.evaluate(t_f)))

    with open(NaiveBayesClassifier.PREPROCESSED_TRAIN, 'w') as writefile:
        writefile.write(','.join(classifier.bag_of_words + ['classlabel']))
        data = classifier.train_feature_vec
        for line in data:
            line = [str(i) for i in line]
            writefile.write(','.join(line) + '\n')

    with open(NaiveBayesClassifier.PREPROCESSED_TEST, 'w') as writefile:
        writefile.write(','.join(classifier.bag_of_words + ['classlabel']))
        data = classifier.test_feature_vec
        for line in data:
            line = [str(i) for i in line]
            writefile.write(','.join(line) + '\n')

    '''
    s =''
    for idx, flag in enumerate(classifier.test_feature_vec[4][:-1]):
        if flag == 1:
            s += classifier.bag_of_words[idx] + ' '
    print(s)
    '''


if __name__ == '__main__':
    main()
