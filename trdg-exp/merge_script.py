import os
import shutil
import re
import random

import cv2
import numpy as np

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def getYoloCoords(xmin, ymin, xmax, ymax, width, height):

    xcen = float((xmin + xmax)) / 2 / width
    ycen = float((ymin + ymax)) / 2 / height

    w = float((xmax - xmin)) / width
    h = float((ymax - ymin)) / height

    return xcen, ycen, w, h

inp_folder = 'unmerged_dataset_skewed'
op_folder = 'merged_dataset_skewed'

images, annotations = [], []

for file_name in os.listdir('./'+inp_folder):
    if '.txt' in file_name:
        annotations.append(file_name)
    elif '.png' in file_name:
        images.append(file_name)

images.sort(key=alphanum_key)
annotations.sort(key=alphanum_key)

lineNumbers = []
currTotal = 0
while currTotal < len(images):
    randomLen = random.choice([3, 4, 5])
    lineNumbers.append(randomLen)
    currTotal += randomLen

if sum(lineNumbers) > len(images):
    lineNumbers[-1] = lineNumbers[-1] - (sum(lineNumbers) - len(images))
elif sum(lineNumbers) < len(images):
    lineNumbers.append(len(images) - sum(lineNumbers))


folder = os.getcwd()+'/'+op_folder
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

i, count = 0, 0
for lineNum in lineNumbers:
    imageBatch, annotationBatch = [], []
    for j in range(i, i + lineNum):
        image = cv2.imread(os.getcwd()+'/'+inp_folder+'/'+images[j])
        imageBatch.append(image)
        annotationBatch.append(os.getcwd()+'/'+inp_folder+'/'+annotations[j])
    
    minWidth = min([image.shape[1] for image in imageBatch])

    imageBatchResized = []
    c_h = 0
    finalAnnFilePath = os.getcwd()+'/'+op_folder+'/'+str(count)+'.txt'
    mergedAnnFile = open(finalAnnFilePath, 'a')

    for img, ann in zip(imageBatch, annotationBatch):
        
        o_w = img.shape[1]
        n_w = minWidth
        o_h = img.shape[0]
        n_h = int(img.shape[0] * minWidth / img.shape[1])
        
        for line in open(ann, 'r').readlines():
            classIndex, o_x1, o_y1, o_x2, o_y2 = [int(float(val)) for val in line.strip().split(' ')]

            n_x1 = (o_x1 * n_w) / o_w
            n_x2 = (o_x2 * n_w) / o_w
            n_y1 = (o_y1 * n_h) / o_h + c_h
            n_y2 = (o_y2 * n_h) / o_h + c_h

            mergedAnnFile.write("{} {} {} {} {}\n".format(classIndex, n_x1, n_y1, n_x2, n_y2))

        c_h += n_h 
        imageBatchResized.append(cv2.resize(img, (n_w, n_h), interpolation = cv2.INTER_CUBIC))

    mergedAnnFile.close()

    mergedImage = cv2.vconcat(imageBatchResized)
    cv2.imwrite(os.getcwd()+'/'+op_folder+'/'+str(count)+'.png', mergedImage)

    mergedHeight = mergedImage.shape[0]
    mergedAnnLines = open(finalAnnFilePath, 'r').readlines()
    
    with open(finalAnnFilePath, 'w') as mergedAnnFile:
        for line in mergedAnnLines:
            classIndex, x1, y1, x2, y2 = [int(float(val)) for val in line.strip().split(' ')]
            xcen, ycen, w, h = getYoloCoords(x1, y1, x2, y2, minWidth, mergedHeight)
            mergedAnnFile.write("{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(
                    classIndex, xcen, ycen, w, h))

    i += lineNum
    count += 1






