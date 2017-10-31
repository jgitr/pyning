# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:57:07 2017

@author: Julian
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:08:35 2017

@author: Julian
"""

import requests, re
from collections import Counter

url = "http://teachingamericanhistory.org/library/document/what-to-the-slave-is-the-fourth-of-july/"
rawhtml = requests.get(url)
# print(rawhtml.text)

# add spaces between elements
#wordlist = ''.join(rawhtml.text)
#print(wordlist)

# make sure these are unique!
textstart = rawhtml.text.find("Mr") - 1
textend = rawhtml.text.find("Foner") 
textsub = rawhtml.text[textstart:textend]


text = list(textsub)
text2 = text # a copy
openbool = False # find and delete <...> combinations
openbackslash = False # find and delete /...> combinations

for i in range(len(text)):
#for i in text:    
#for i in range(0,50):
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
#plocation = s.find("/p>")   
expression = "(\\xa0em)|(p>\\np>)|(br >\\n)|(thugsem>)|(em>)|(\\xa0)" 
cleantext = re.sub(expression, '', s)       


# Count in dictionary
dat = list(cleantext.split())
dict = {}
for i in range(len(dat)):
    print(i)
    word = dat[i]
    dict[word] = dat.count(word)
    continue

hierarchy = [(k, dict[k]) for k in sorted(dict, key=dict.get, reverse=True)]





