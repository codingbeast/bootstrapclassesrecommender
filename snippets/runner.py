from zipfile import ZipFile
import os
import glob
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import shutil
import json
import requests
from clint.textui import progress

res = requests.get("https://raw.githubusercontent.com/twbs/bootstrap/main/README.md")
link = re.findall("[Download the latest release]((.*?))\n-",res.text)
finalLink =''
for i in link:
    if "https://github.com/twbs/bootstrap/archive/" in i[1]:
        finalLink = re.search("(?P<url>https?://[^\s]+)", i[1]).group("url")[:-1]
        
print("downloading from ",finalLink)
version = finalLink.split("/v")[-1].split(".zip")[0]
filename = "bootstrap-{}".format(version)

r = requests.get(finalLink, stream=True)
with open(filename + ".zip", 'wb') as f:
    total_length = int(r.headers.get('content-length'))
    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
        if chunk:
            f.write(chunk)
            f.flush()
#unzip the file 

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
