from pyspark.mllib.feature import HashingTF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import SVMWithSGD

from pyspark import SparkContext, SparkConf
conf = SparkConf().setMaster("local[*]").setAppName("Naive_Bayes")
sc   = SparkContext(conf=conf)
print "Running Spark Version %s" % (sc.version)

#word to vector space converter, limit to 10000 words
htf = HashingTF(10000)

# ngram function
def to_2gram(wordlist):
	newlist=[]
	for i in range(len(wordlist)-1):
		newlist.append(wordlist[i]+wordlist[i+1])
	return wordlist + newlist


#let 1 - positive class, 0 - negative class
#tokenize sentences and transform them into vector space model

positiveData = sc.textFile("Positive.txt")
posdata = positiveData.map(lambda text : LabeledPoint(1, htf.transform(to_2gram(text.replace(',','').replace('.','').replace('-','').replace('?','').replace('!',' ').lower().split(" ")))))
print "No. of Positive Sentences: " + str(posdata.count())
posdata.persist()

negativeData = sc.textFile("Negative.txt")
negdata = negativeData.map(lambda text : LabeledPoint(0, htf.transform(to_2gram(text.replace(',','').replace('.','').replace('-','').replace('?','').replace('!',' ').lower().split(" ")))))
print "No. of Negative Sentences: " + str(negdata.count())
negdata.persist()

# Split positive and negative data 60/40 into training and test data sets
pt = sc.textFile("tPositive.txt")
nt = sc.textFile("tNegative.txt")
ptrain = posdata
ptest = pt.map(lambda text : LabeledPoint(1, htf.transform(to_2gram(text.replace(',','').replace('.','').replace('-','').replace('?','').replace('!',' ').lower().split(" ")))))
ntrain = negdata
ntest = nt.map(lambda text : LabeledPoint(0, htf.transform(to_2gram(text.replace(',','').replace('.','').replace('-','').replace('?','').replace('!',' ').lower().split(" ")))))

#union train data with positive and negative sentences
trainh = ptrain.union(ntrain)
#union test data with positive and negative sentences
testh = ptest.union(ntest)

# Train a Naive Bayes model on the training data
model = SVMWithSGD.train(trainh,iterations=100)

# Compare predicted labels to actual labels
prediction_and_labels = testh.map(lambda point: (model.predict(point.features), point.label))

# Write prediction into file
# prediction_and_labels.saveAsTextFile("Output")

# Filter to only correct predictions
correct = prediction_and_labels.filter(lambda (predicted, actual): predicted == actual)

# Calculate and print accuracy rate
accuracy = correct.count() / float(testh.count())

print "Classifier correctly predicted category " + str(accuracy * 100) + " percent of the time"