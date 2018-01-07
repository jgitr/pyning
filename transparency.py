# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 21:21:58 2018

@author: Julian
"""

from PIL import Image, ImageDraw

img = Image.new('RGBA',(100, 100))

draw = ImageDraw.Draw(img)
draw.ellipse((25, 25, 75, 75), fill=(255, 0, 0))

img.save('test.gif', 'GIF', transparency=0)
