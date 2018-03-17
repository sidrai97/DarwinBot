import textblob

a=textblob.TextBlob("coorrect")
b=a.correct()
print(type(str(b)))