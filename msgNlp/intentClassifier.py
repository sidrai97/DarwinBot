from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

with open('./train_data/train.json', 'r') as fp:
    cl = NaiveBayesClassifier(fp, format="json")

while True:
    ip=input('enter message:')
    blob=TextBlob(ip, classifier=cl)
    op=blob.classify()
    prob_dist=cl.prob_classify(ip)
    print('Classified Intent => {} '.format(op))