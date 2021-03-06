"""
Character Detection
(Due date: March 8th, 11: 59 P.M.)

The goal of this task is to experiment with template matching techniques. Specifically, the task is to find ALL of
the coordinates where a specific character appears using template matching.

There are 3 sub tasks:
1. Detect character 'a'.
2. Detect character 'b'.
3. Detect character 'c'.

You need to customize your own templates. The templates containing character 'a', 'b' and 'c' should be named as
'a.jpg', 'b.jpg', 'c.jpg' and stored in './data/' folder.

Please complete all the functions that are labelled with '# TODO'. Whem implementing the functions,
comment the lines 'raise NotImplementedError' instead of deleting them. The functions defined in utils.py
and the functions you implement in task1.py are of great help.

Hints: You might want to try using the edge detectors to detect edges in both the image and the template image,
and perform template matching using the outputs of edge detectors. Edges preserve shapes and sizes of characters,
which are important for template matching. Edges also eliminate the influence of colors and noises.

Do NOT modify the code provided.
Do NOT use any API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import any library (function, module, etc.).
"""


import argparse
import json
import os

import numpy as np
import cv2

from utils import *
from task1 import *   # you could modify this line

thresholds ={
    "./data/a.jpg":0.7,
    "./data/b.jpg":0.85,
    "./data/c.jpg":0.7
}


def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img_path", type=str, default="./data/characters.jpg",
        help="path to the image used for character detection (do not change this arg)")
    parser.add_argument(
        "--template_path", type=str, default="",
        choices=["./data/a.jpg", "./data/b.jpg", "./data/c.jpg"],
        help="path to the template image")
    parser.add_argument(
        "--result_saving_directory", dest="rs_directory", type=str, default="./results/",
        help="directory to which results are saved (do not change this arg)")
    args = parser.parse_args()
    return args


def detect(img, template,threshold):
    """Detect a given character, i.e., the character in the template image.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        coordinates: list (tuple), a list whose elements are coordinates where the character appears.
            format of the tuple: (x (int), y (int)), x and y are integers.
            x: row that the character appears (starts from 0).
            y: column that the character appears (starts from 0).
    """
    # TODO: implement this function.
    img_r = len(img)
    img_c = len(img[0])
    temp_r = len(template)
    temp_c = len(template[0])
    diff = []
    diff_elem = []
    sum = 0
    print("Please wait for 5-6 minutes")
    for i in range(0,img_r - (temp_r-1)):
        for j in range(0, img_c - (temp_c-1)):
            img_patch = crop(img,i,i+temp_r,j,j+temp_c)
            sum = Ncc(img_patch,template)
            diff_elem.append(sum)
            sum = 0
        diff.append(diff_elem)
        diff_elem=[]
    x = len(diff)
    y = len(diff[0])
    coordinates = []
    img2 = img
    for i in range(0,x):
        for j in range(0,y):
            if(diff[i][j]>threshold):
                min = diff[i][j]
                l_x,l_y = i,j
                if(len(coordinates) >= 1):
                    last = coordinates[-1]
                    ty = l_y - last[1]
                    tx = l_x - last[0]
                    if ty+tx !=1 :
                        coordinates.append((l_x,l_y))
                else:
                    coordinates.append((l_x, l_y))
    if(len(coordinates) > 20):
        del(coordinates[-1])
    #draw_rectangle(coordinates,temp_r,temp_c)
    #raise NotImplementedError
    return coordinates

def Ncc(img_patch,template):
'''
Computes Normalized cross correlation 
'''
    m,n=0,0
    imean=0
    tmean=0
    deno1=0
    deno2=0
    ncc_sum =0
    imgs = copy.deepcopy(img_patch)
    temp = copy.deepcopy(template)
    imean = Mean(imgs)
    tmean = Mean(temp)
    m=len(imgs)
    n=len(imgs[0])
    for i in range(0,m):
        for j in range(0,n):
            imgs[i][j] = imgs[i][j] - imean
            temp[i][j] = temp[i][j] - tmean
    for i in range(0,m):
        for j in range(0,n):
            deno1 = deno1 + (imgs[i][j])**2
            deno2 = deno2 + (temp[i][j])**2
    deno1 = np.sqrt(deno1)
    deno2 = np.sqrt(deno2)
    for i in range(0,m):
        for j in range(0,n):
            if(deno1!=0):
                imgs[i][j] = imgs[i][j]/deno1
            temp[i][j] = temp[i][j]/deno2
    ncc = elementwise_mul(imgs,temp)
    for i in range(0,m):
        for j in range(0,n):
            ncc_sum = ncc_sum + ncc[i][j]
    return ncc_sum
    #raise NotImplementedError

'''
def draw_rectangle(coordinates,temp_r,temp_c):
    new_img = cv2.imread("./data/proj1-task2.jpg")
    for i, num in enumerate(coordinates):
        cv2.rectangle(new_img,(num[1],num[0]),(num[1]+temp_c,num[0]+temp_r),(255,0,0),2)
        cv2.imshow("rectangle",new_img)
        k = cv2.waitKey(0)
'''

def Mean(a):
'''
Computes mean
'''
    sum=0
    m = len(a)
    n = len(a[0])
    for i in range(0,m):
        for j in range(0,n):
            sum = sum + a[i][j]
    return sum /(m*n)

def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def main():
    args = parse_args()

    img = read_image(args.img_path)
    template = read_image(args.template_path)
    threshold = thresholds[args.template_path]
    coordinates = detect(img, template,threshold)
    print("Done computing")
    template_name = "{}.json".format(os.path.splitext(os.path.split(args.template_path)[1])[0])
    save_results(coordinates, template, template_name, args.rs_directory)


if __name__ == "__main__":
    main()
