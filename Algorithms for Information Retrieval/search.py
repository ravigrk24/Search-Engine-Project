import os 
import sys
from elasticsearch import Elasticsearch
import pandas as pd
import csv
files= os.listdir("./TelevisionNews")
es = Elasticsearch(HOST="http://localhost", PORT=9200)
es = Elasticsearch()
es.indices.delete(index="air")
es.indices.create(index="air")
count=0

for f in files:
	with open("./TelevisionNews/"+f) as csvfile:
		readCSV=csv.reader(csvfile,delimiter=',')
		for ind,row in enumerate(readCSV):
			if(len(row)==7):		
				d=dict()
				d["URL"]=row[0]
				d["MatchDateTime"]=row[1]
				d["Station"]=row[2]
				d["Show"]=row[3]
				d["IAShowID"]=row[4]
				d["IAPreviewThumb"]=row[5]
				d["Snippet"]=row[6]
				es.index(index="air", doc_type="text", id=f+str(ind), body=d)
body = {
    "from":0,
    "size":5,
    "query": {
        "match": {
            "Snippet":"barack obama"
        }
    }
}
res = es.search(index="air", body=body)
print(res)
