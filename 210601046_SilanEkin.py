# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 20:36:06 2024

@author: silan
"""

import cv2
import numpy as np

#Resmin kenarlarını kaldırmak için
def removeBorder(img):
    return img[30:len(img) - 20, 30:len(img[0]) - 20]

#Üç rengi birleştirir
def getColor(blue, green, red, level):
    img2 = np.zeros((len(red), len(red[0]), 3), np.uint8)
    for i in range(len(img2)):
        for j in range(len(img2[0])):
            img2[i][j][0] = blue[i][j] / (level + 1)
            img2[i][j][1] = green[i][j] / (level + 1)
            img2[i][j][2] = red[i][j] / (level + 1)
    return img2

# Üç görüntüyü birleştirme
def getAllFilters(img):
    filters = []
    for k in range(3):
        img2 = np.zeros((len(img) // 3, len(img[0]) - 20, 1), np.uint8)
        for i in range(len(img2)):
            for j in range(len(img2[0])):
                if k == 0:
                    img2[i][j] = img[i + (2 * len(img2))][j]
                if k == 1:
                    img2[i][j] = img[i + len(img2)][j]
                if k == 2:
                    img2[i][j] = img[i][j]
        filters.append(img2)
    return filters


def getAllPyramids(img, level):
    G = img.copy()
    gpA = [G]
    for i in range(level):
        G = cv2.pyrDown(G)
        gpA.append(G)
    return gpA

def reconstruct(colorPyramid, level):
    im = colorPyramid[level]
    for i in range(len(colorPyramid) - 2, -1, -1):
        im = cv2.pyrUp(im)
        im = cv2.resize(im, (colorPyramid[i].shape[1], colorPyramid[i].shape[0]))
        im = cv2.add(im, colorPyramid[i])
    return im

# Birden fazla resmi işlemek için ana döngü
def process_images(image_paths):
    for img_path in image_paths:
        img = cv2.imread(img_path, 0)
        if img is None:
            print("Error: Could not load image. Please check the path:", img_path)
            continue

        filters = getAllFilters(img)
        pyramids = []
        for filter in filters:
            pyramids.append(getAllPyramids(filter, level=4))
        colorPyramid = []
        for i in range(len(pyramids[0])):
            colorPyramid.append(getColor(pyramids[2][i], pyramids[1][i], pyramids[0][i], level=4))

        im = reconstruct(colorPyramid, level=4)
        im = removeBorder(im)

        cv2.imshow('Image', im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#resimlerin dosya yolu
image_paths = ["C:/Users/silan/.spyder-py3/gorntuisleme/00125v.jpg", "C:/Users/silan/.spyder-py3/gorntuisleme/00149v.jpg", "C:/Users/silan/.spyder-py3/gorntuisleme/00153v.jpg",
               "C:/Users/silan/.spyder-py3/gorntuisleme/00351v.jpg", "C:/Users/silan/.spyder-py3/gorntuisleme/00398v.jpg", "C:/Users/silan/.spyder-py3/gorntuisleme/01112v.jpg"]

#işlemi çağırma
process_images(image_paths)
