import os
import sys
import time
import resource
from BTrees.OOBTree import OOBTree
import nltk 
from nltk.stem import WordNetLemmatizer
lem=WordNetLemmatizer()
from nltk.stem import PorterStemmer 
ps = PorterStemmer() 
import pandas as pd
files= os.listdir("./TelevisionNews")
files_count= len(files)
print(type(files),files_count)
id_name={}
dictionary={}
import pickle
import csv

max_rec = 0x100000
import math
def ntf(d):
	s=0
	for i in d.values():
		s=s+i
	return s


"""
N=0
df=dict()
tf=dict()
resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
sys.setrecursionlimit(max_rec)
for f in files:
	tf[f[:-4]]=dict()
	with open("./TelevisionNews/"+f) as csvfile:
			readCSV=csv.reader(csvfile,delimiter=',')
			t = OOBTree()
			for ind,row in enumerate(readCSV):
				pos=0
				N=N+1
				tf[f[:-4]][ind]=dict()
				if(len(row)==7):
					for j in range(len(row)):
						if(j==6):
							l=nltk.tokenize.WhitespaceTokenizer().tokenize(row[j])
							l = [nltk.stem.WordNetLemmatizer().lemmatize(word) for word in l]
							l=[k.lower() for k in l] 
							
							for k in l:
								#ps.stem(k)
								if(k in tf[f[:-4]][ind]):
									tf[f[:-4]][ind][k]=tf[f[:-4]][ind][k]+1
								else:
									tf[f[:-4]][ind][k]=1
								if(k in df):
									df[k]=df[k]+1
								else:
									df[k]=1
								if(t.has_key(k)):
									if( ind in t[k]):
										t[k][ind].append(pos)
										pos=pos+1	
									else:
										ll=list()
										ll.append(pos)
										pos=pos+1
										t[k][ind]=ll
								else:
									ll=list()
									ll.append(pos)
									pos=pos+1
									dd=dict()
									dd[ind]=ll
									t[k]=dd	
						else:
							#ps.stem(row[j])
							if(row[j] in tf[f[:-4]][ind]):
								tf[f[:-4]][ind][row[j]]=tf[f[:-4]][ind][row[j]]+1
							else:
								tf[f[:-4]][ind][row[j]]=1
							if(row[j] in df):
								df[row[j]]=df[row[j]]+1
							else:
								df[row[j]]=1
							if(t.has_key(row[j])):
								if ind in t[row[j]]:
									t[row[j]][ind].append(pos)
									pos=pos+1
								else:
									ll=list()
									ll.append(pos)
									pos=pos+1
									t[row[j]][ind]=ll
							else:
								ll=list()
								ll.append(pos)
								pos=pos+1
								dd=dict()
								dd[ind]=ll
								t[row[j]]=dd
			afile = open(r"./"+f[:-4]+".pkl", 'wb')
			pickle.dump(t, afile)
			afile.close()
end=time.time()
df["N"]=N
afile = open(r"./"+"tf"+".pkl", 'wb')
pickle.dump(tf, afile)
afile.close()
afile = open(r"./"+"df"+".pkl", 'wb')
pickle.dump(df, afile)
afile.close()
"""

file2 = open(r"df.pkl", 'rb')
new_d = pickle.load(file2)
file2.close()

file1 = open(r"df.pkl", 'rb')
df = pickle.load(file1)
file1.close()
file2 = open(r"tf.pkl", 'rb')
tf = pickle.load(file2)
file2.close()



def editDistDP(str1):
	if(str1 in df):
		return str1
	maxi=1000000000
	res=str1
	m=len(str1)
	for str2 in df:
		n=len(str2)
		dp = [[0 for x in range(n + 1)] for x in range(m + 1)] 
		for i in range(m + 1): 
			for j in range(n + 1):
				if(i == 0): 
					dp[i][j] = j   
				elif(j==0): 
					dp[i][j] = i   
				elif(str1[i-1] == str2[j-1]): 
					dp[i][j] = dp[i-1][j-1] 
				else: 
					dp[i][j] = 1 + min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])    
		if(dp[m][n]<maxi):
			res=str2
			maxi=dp[m][n]
		if(maxi==0):
			return res;
	return res
l=list()
#print(new_d["warming"],new_d["greenhouse"],new_d["gas"])
#query="greenhouses gasses and global warming "
query=input("ENTER YOUR QUERY\n")
start=time.time()
query=nltk.tokenize.WhitespaceTokenizer().tokenize(query)
query=[nltk.stem.WordNetLemmatizer().lemmatize(word) for word in query]

query=[i.lower() for i in query]
"""for i,q in enumerate(query):
	query[i]=editDistDP(q)"""
ql=[query.count(i)/len(query) for i in query]
for i in range(len(ql)):
	if(query[i] in df):
		ql[i]=ql[i]*math.log(df["N"]/df[query[i]])
	else:
		ql[i]=0
a=0
for i in ql:
	a=a+i*i
a=pow(a,0.5)
for f in files:
	for i,row in enumerate(tf[f[:-4]]):
		s=ntf(tf[f[:-4]][i])
		#print(s)
		ll=[0]*len(ql)
		for qi,q in enumerate(query):
			if(q in tf[f[:-4]][i]):
				ll[qi]=tf[f[:-4]][i][q]/s
				ll[qi]*=math.log(df["N"]/df[q])
		b=0
		for j in ll:
			b=b+j*j
		b=pow(b,0.5)
		if(b!=0):
			s=0
			for j in range(len(ql)):
				s+=ql[j]*ll[j]
			s=s/a
			s=s/b
			s=round(s,10)
			res=list()
			res.append(f)
			res.append(i)
			res.append(s)
			l.append(res)
l.sort(key=lambda x:x[2])
l.reverse()

for i in range(10):
	if(i>=len(l)):
		print("no entries")
		break
	with open("./TelevisionNews/"+l[i][0]) as csvfile:
		readCSV=csv.reader(csvfile,delimiter=',')
		row=[i for i in readCSV]
		print("doc:",l[i][0],"\trow:",l[i][1],"\tURL:",row[l[i][1]][0],"MatchDateTime\t:",row[l[i][1]][1],"Station\t:",row[l[i][1]][2],"\tShow:",row[l[i][1]][3],"\tIAShowID:",row[l[i][1]][4],"\tIAPreviewThumb:",row[l[i][1]][5],"\tSnippet:",row[l[i][1]][6],"\n")

end=time.time()
print("time taken: ",end-start)	

