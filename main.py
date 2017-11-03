# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:57:07 2017

@author: Julian
"""

import matplotlib.pyplot as plt
import requests, re


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

nText = range(len(text))
for i in nText:
    
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

# Some expressions still left
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

def valueSelection(dictionary, length): # length is length of highest value vector
    
    # Test input
    lengthDict = len(dictionary)
    if length > lengthDict:
        return print("length is longer than dictionary length");
    else:
        d = dictionary
        items = [(v, k) for k, v in d.items()]
        items.sort()
        items.reverse()   
        itemsOut = [(k, v) for v, k in items]
    
        highest = itemsOut[0:length]
        dd = dict(highest)
        wanted_keys = dd.keys()
        dictshow = dict((k, d[k]) for k in wanted_keys if k in d)

        return dictshow;
    
dictshow = valueSelection(dictionary = dict1, length = 15)

# Select highest ones to show
#allhighest = items[0:10]
#dd = dict(allhighest)
#wanted_keys = dd.keys() # The keys you want
#longdict = dict1
#dictshow = dict((k, longdict[k]) for k in wanted_keys if k in longdict)

# Plot
n = range(len(dictshow))
plt.bar(n, dictshow.values(), align='center')
plt.xticks(n, dictshow.keys())

plt.savefig("plot.png")