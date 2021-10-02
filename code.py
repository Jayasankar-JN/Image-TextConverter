#importing libraries
import cv2
import numpy as np
import os
import math

#reading image and load it in grayscale mode
file_name = input("Enter the Image filename (in png format) : ")
org_img = cv2.imread(file_name,0)
img = org_img.copy()

# removing background of image

#floor function returns the greatest integer less than or equal to input
n = math.floor(img.shape[0]/2)
m = math.floor(img.shape[1]/2)
pt1 = 0
pt2 = 0
for i in range(m):
    if(img[n][i] == 255):
        pt1 = i
        break
for i in range(n):
    if(img[i][m] == 255):
        pt2 = i
        break
# 3 -->> offset
img = img[pt1+3:-(pt1+3),pt2+3:-(pt2+3)]
org_img = img.copy()


# highlighting image
img = (img//255)*255


# making array
img_array = img//255
img_array = abs(img_array - 1)
img_array = img_array.sum(axis = 1)

# darkening lines for drawing contours
m_img = img.copy()
for i in range(len(img_array)):
    if(img_array[i] != 0):
        m_img = cv2.line(m_img,(img.shape[1],i),(0,i),(0,255,0),2)

# Invert colors for contour detection
m_img = 255 - m_img

# Detect contours
contours, hierarchy = cv2.findContours(m_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#make list of lines
lines = []
for i in contours:
    lines.append(org_img[i[0][0][1]:i[1][0][1],:])


#extracting words from each line 
words = []
for i in lines:
    img_array = i//255
    img_array = abs(img_array - 1)
    img_array = img_array.sum(axis = 0)
    m_img = i.copy()
    for j in range(len(img_array)):
        if(img_array[j] != 0):
            m_img = cv2.line(m_img,(j,0),(j,i.shape[0]),(0,255,0),1)
    # Invert colors for contour detection
    m_img = 255 - m_img
    contours, hierarchy = cv2.findContours(m_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(m_img,contours,-1,(0,255,0),4)
    for j in contours:
        words.append(i[:,j[0][0][0]:j[2][0][0]])


#Assigning directory to lines,words 

directory1 = './Lines/Line_'
directory2 = './Words/Word_'




for i in range(len(lines)):
    cv2.imwrite(directory1 + str(i) + ".png",lines[i])


for i in range(len(words)):
    cv2.imwrite(directory2 + str(i) + ".png",words[i])




print("Outputs are sucessfully placed inside the corresponding directories!")
