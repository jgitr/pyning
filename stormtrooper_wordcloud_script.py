# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 20:19:52 2017

@author: Julian
"""

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS



d = "C:/Users/Julian/pyning"


# Read the whole text.
text = open(path.join(d, 'Output.txt')).read()

# Mask
stormtrooper_mask = np.array(Image.open(path.join(d, "stormtrooper_mask.png")))

# Optional additional stopwords
stopwords = set(STOPWORDS)
stopwords.add("said")


wc = WordCloud(background_color="white", max_words=1000, mask=stormtrooper_mask,
stopwords=stopwords)


# generate word cloud
wc.generate(text)


# store to file
wc.to_file(path.join(d, "a_new_hope.png"))


# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(stormtrooper_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()
plt.savefig("stormtrooper.png")
