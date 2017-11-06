# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:57:07 2017

@author: Julian
"""

import matplotlib.pyplot as plt
import requests, re
from nltk.corpus import stopwords


# Get HTML
url = "http://teachingamericanhistory.org/library/document/what-to-the-slave-is-the-fourth-of-july/"
rawhtml = requests.get(url)


# make sure these are unique!
#textstart = rawhtml.text.find("Mr") - 1
#textend = rawhtml.text.find("Foner") 
#textsub = rawhtml.text[textstart:textend]
#text = list(textsub)

text = list(rawhtml.text)


# find and delete <...> combinations
# find and delete /...> combinations
# Takes only lists as input
# Returns list as output

def SearchAndReplaceSeq(html, opensign, closesign):
    
        openbool = False
        nText = range(len(text))
        
        for i in nText:
            
            print("i = ", i)
            print("outer loop")
            
            if text[i] in opensign:
                loc = opensign.index('<')
                openbool = True
                print("deleting ", text[i])  
                text[i] = "" # delete
                
                while openbool:         
                            print("inner loop")
                            
                            if text[i] != closesign[loc]:
                                print(i, "deleting ", text[i])  
                                text[i] = ""
                                i += 1
                            
                            else:
                                print(i, "deleting ", text[i])  
                                text[i] = ""
                                openbool = False
                                i += 1
                                                        
                

                #continue # switch to next mark, first one is always open

            else:
                print("keeping", text[i])
                print("outer loop down")
                continue #i += 1     
                
        return(text); 

                     
textout = SearchAndReplaceSeq(html = text, opensign = ['<', '/', '{'], closesign = ['>', '>', '}'])

s = "".join(textout)   


# Some expressions still left
# Differ between quotes!
expression = "(\\xa0em)|(p>\\np>)|(br >\\n)|(thugsem>)|(em>)|(\\xa0)|[()]|(\“)|(\”)|(\“)|(\”)|(\,|\.|-|\;|\<|\>)|(\\n)|(\\t)"
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


# Filter Stopwords
keys = list(dict1)
filtered_words = [word for word in keys if word not in stopwords.words('english')]
dict2 = dict((k, dict1[k]) for k in filtered_words if k in filtered_words)

#keys in stopwords.words("english")

# Resort in list
# Reconvert to dictionary

def valueSelection(dictionary, length, startindex = 0): # length is length of highest consecutive value vector
    
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
    
        highest = itemsOut[startindex:startindex + length]
        dd = dict(highest)
        wanted_keys = dd.keys()
        dictshow = dict((k, d[k]) for k in wanted_keys if k in d)

        return dictshow;
    
dictshow = valueSelection(dictionary = dict2, length = 10, startindex = 0)



# Plot
n = range(len(dictshow))
plt.bar(n, dictshow.values(), align='center')
plt.xticks(n, dictshow.keys())

plt.savefig("plot.png")
