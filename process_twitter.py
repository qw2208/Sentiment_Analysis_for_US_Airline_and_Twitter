# coding: utf-8
import csv

# csvfile = file('TwitterAirline.csv','rb')
# reader = csv.reader(csvfile)
reader = csv.reader(open("Airline-Sentiment-2-w-AA.csv", 'rU'), dialect='excel')

f0 = open('tNegative.txt','w')
f1 = open('tPositive.txt','w')

for line in reader:
	if line[5] == 'negative':
		f0.write(line[14]+'\n')
	elif line[5] == 'positive':
		f1.write(line[14]+'\n')

f0.close()
f1.close()