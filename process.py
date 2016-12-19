# coding: utf-8
import csv

csvfile = file('training.1600000.processed.noemoticon.csv','rb')
reader = csv.reader(csvfile)

f0 = open('Negative.txt','w')
f1 = open('Positive.txt','w')

for line in reader:
	if line[0] == '0':
		f0.write(line[5]+'\n')
	elif line[0] == '4':
		f1.write(line[5]+'\n')


csvfile = file('Sentiment Analysis Dataset.csv','rb')
reader = csv.reader(csvfile)
for line in reader:
	if line[1] == '0':
		f0.write(line[3]+'\n')
	elif line[1] == '1':
		f1.write(line[3]+'\n')

f0.close()
f1.close()