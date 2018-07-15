import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import bz2
import random
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pickle



class GetSentiment(object):
    def __init__(self):
        pass

    def get_review(self):
        print("Enter the review to get Sentiment:")
        self.review = input()
        # return self.review
    
    # def print_comment(self):
    #     print(self.review)

    def get_classifier(self):
        open_model = open('/home/blackpanther/coding/Github Portfolio/Final/Final Portfolio/Sentiment Analysis Amazon Reviews/model.pickle','rb')
        classifierVC = pickle.load(open_model)
        open_model.close()
        return classifierVC
    
    def get_vector(self):
        open_vc = open('/home/blackpanther/coding/Github Portfolio/Final/Final Portfolio/Sentiment Analysis Amazon Reviews/save_cv.pickle','rb')
        vc = pickle.load(open_vc)
        open_vc.close()
        return vc

    def process_review(self):
        cor=[]
        ps = PorterStemmer()
        rev = re.sub('[^a-zA-Z]',' ',self.review)
        rev = rev.lower()
        rev = rev.split()
        rev = [ps.stem(word) for word in rev if not word in set(stopwords.words('english'))]
        rev = ' '.join(rev)
        cor.append(rev)
        cor = self.get_vector().transform(cor).toarray()
        output = self.get_classifier().predict(cor)[0]
        return output

    def review_classifier(self):
        if self.process_review() == 1:
            print("Your Customer seems to be HAPPY about the purchase")
        else:
            print("Your customer is NOT HAPPY about the purchase")


if __name__ == "__main__":
    s = GetSentiment()
    s.get_review()
    s.process_review()
    s.review_classifier()
    
