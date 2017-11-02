# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:57:07 2017

@author: Julian
"""

#import numpy as np
import matplotlib.pyplot as plt
import requests, re
#import pandas

# Get HTML
url = "http://teachingamericanhistory.org/library/document/what-to-the-slave-is-the-fourth-of-july/"
rawhtml = requests.get(url)


# make sure these are unique!
textstart = rawhtml.text.find("Mr") - 1
textend = rawhtml.text.find("Foner") 
textsub = rawhtml.text[textstart:textend]


text = list(textsub)
openbool = False # find and delete <...> combinations
openbackslash = False # find and delete /...> combinations

for i in range(len(text)):
    
    print("i = ", i)
    
    if text[i] == '<':
        openbool = True
        print("deleting ", text[i])  
        text[i] = "" # delete
        continue
        
        while openbool:         
                   
                    if text[i] == '>':
                        print("deleting ", text[i])  
                        text[i] = ""
                        openbool = False
                        break
                    
                    else:
                        print("deleting ", text[i])  
                        text[i] = ""
                        continue # switch to next mark, first one is always open

    if text[i] == '/':
        openbackslash = True
        print("deleting ", text[i])  
        text[i] = "" # delete
        continue
        
        while openbackslash:         
                   
                    if text[i] == '>':
                        print("deleting ", text[i])  
                        text[i] = ""
                        openbackslash = False
                        break
                    
                    else:
                        print("deleting ", text[i])  
                        text[i] = ""
                        continue # switch to next mark, first one is always open


    else:
        print("keeping", text[i])
        continue #i += 1     
             


s = "".join(text)   

# \xa0em> and p>\np> and br >\n and thugsem> and em> and \xa0 still left
expression = "(\\xa0em)|(p>\\np>)|(br >\\n)|(thugsem>)|(em>)|(\\xa0)|[()]|(\“)|(\”)|(\“)|(\”)|(\,|\.|-|\;|\<|\>)"
cleantextCAP = re.sub(expression, '', s)
cleantext = cleantextCAP.lower()       


# Count and create dictionary
dat = list(cleantext.split())
dict1 = {}
for i in range(len(dat)):
    print(i)
    word = dat[i]
    dict1[word] = dat.count(word)
    continue


# Resort in list
d = dict1
items = [(v, k) for k, v in d.items()]
items.sort()
items.reverse()   
items = [(k, v) for v, k in items]

# Select highest ones to show
allhighest = items[0:10]
dd = dict(allhighest)
dd.keys()
wanted_keys = dd.keys() # The keys you want
longdict = dict1
dictshow = dict((k, longdict[k]) for k in wanted_keys if k in longdict)

# Plot
n = range(len(dictshow))
plt.bar(n, dictshow.values(), align='center')
plt.xticks(n, dictshow.keys())

