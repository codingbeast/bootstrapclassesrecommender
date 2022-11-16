from zipfile import ZipFile
import os
import glob
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import shutil
import json

#unzip the file 
filename = "bootstrap-5.0.2"
unzipPath = os.getcwd()
with ZipFile(filename + ".zip", 'r') as zObject:
    zObject.extractall(unzipPath)
    
    
#detect all css files
files = [i for i in glob.glob(os.path.join(filename,"dist","css","*.css"))]



#read and extract the all classes name
finalset = []
for sample in files:
    with open(sample, 'r', encoding='utf-8') as reader:
        data = reader.read()
    sepdata = []
    for i in word_tokenize(data):
        if i.startswith(".") and not i.replace(".","").isnumeric():
            if i.replace(".",""):
                sepdata.append(i.replace(".",""))
    sepdata = list(set(sepdata))
    finalset.extend(sepdata)
    #break
#save the classes in file
dictset = {}
for i in finalset:
    dictset[i] = {
		"scope": "html",
		"prefix": [i],
		"body": [i],
	}
    
with open('snippets.code-snippets', 'w') as fp:
    json.dump(dictset, fp, indent=4)
    
#remove the zip file and old folder
os.remove(filename + ".zip")
shutil.rmtree(filename)
