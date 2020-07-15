# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 15:06:56 2020

@author: dthakur
"""


import io
import sys
import matplotlib.pyplot as plt
from math import sqrt
from PIL import Image

def readImageToArray(image):    
    
    pixel = image.load()
    
    width, height = image.size
    
    all_pixels = []
    
    for x in range(width):
        for y in range(height):
            value= pixel[x,y]
            all_pixels.append(value)
    return all_pixels

def sortedDictionaryOfPixels(imagearray):
    dictionary = {} 
    for pxl in imagearray:
        r,g,b = pxl
        
        r = int(r/20)*20
        g = int(g/20)*20
        b = int(b/20)*20
        binkey = (round(r/255,2),round(g/255,2),round(b/255,2))
        if binkey in dictionary:
            dictionary[binkey] +=1
        else:
            dictionary[binkey] = 1
                
    newA = sorted(dictionary, key=dictionary.get, reverse=True)[:25]
    sortedKeyList = sorted(newA, key = lambda p: sqrt(p[0]**2+p[1]**2+p[2]**2), reverse = True)
    sortedDict2 = {}
    for val in sortedKeyList:
        sortedDict2[val] = dictionary[val]
    newDict = optimizedAlgo(sortedDict2)
    return list(newDict.keys())


def plotAndSave(sortedDict, length):
    
    keys = sortedDict
    value = 100
    trial = list(range(1,length+1))
    plt.bar(trial,value,color=keys,width = 0.8,align='edge')
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    im = Image.open(buf)
    return im

def combineAndSave(image, palette):
    images = [image, palette]
    widths = image.size[0]
    heights= image.size[1]+palette.size[1]
    new_im = Image.new('RGB', (widths, heights))
    x_offset = 0
    for im in images:
      new_im.paste(im, (0,x_offset))
      x_offset += im.size[1]

    new_im.save('result.jpg')
    return new_im

def euclddist(prev_key,key):
    r1,g1,b1 = prev_key
    r2, g2,b2 = key
    dist = sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
    return dist
    
    
def optimizedAlgo(dct):
    dist = 0.20
    prev_key = 0
    cntr = 0;
    new_dct = {}
    for key in dct:
        if cntr == 0:
            cntr += 1
            new_dct[key] =dct[key]
            prev_key = key
            continue
        r1,g1,b1 = prev_key
        r2, g2,b2 = key
        calcdist = euclddist(prev_key,key)
        if(calcdist < dist ):
            continue
        else:
            new_dct[key] = dct[key]
            prev_key = key  
    return new_dct
        
        
        

def main():
    imageLocation = r"input.jpg"
    if len(sys.argv)==2:
        imageLocation = sys.argv[1]
    image = Image.open(imageLocation)
    imagearray = readImageToArray(image)
    sortedDict = sortedDictionaryOfPixels(imagearray)
    palette = plotAndSave(sortedDict,len(sortedDict))
    width, height = palette.size
    palette = palette.crop((width*0.1,0,width*0.9,height))
    palette = palette.resize((image.size[0],int(image.size[1]/3)))
    result=combineAndSave(image,palette)
    result.show()
    
    
    

if __name__ == "__main__":
    main()
