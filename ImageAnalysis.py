import os
os.chdir('/Users/yebi/Library/CloudStorage/OneDrive-VirginiaTech/Research/Codes/research/BCS/BodyWeight') ## Change this into ur own folder

import argparse
parser = argparse.ArgumentParser(description =
                                 'Extracting image descriptors from image')
parser.add_argument('day', help = 'day info.')

args = parser.parse_args()


import sys
# from PIL import Image # Python Imaging Library
import matplotlib.pyplot as plt #used to show images
import matplotlib.pyplot as plt #used to show images

# from google.colab.patches import cv2_imshow
import imutils
from scipy import stats # summarize data

import os
import csv
from scipy.spatial import distance as dist
from imutils import perspective
import numpy as np
# import argparse
import cv2
import pandas as pd
                                                            ## If run for dataset in GitHub:
rootdir = "/Volumes/MyPassport1"                            ## Change rootdir into "./"     ####################
temp_dep = "/Volumes/MyPassport1/" + args.day + "/depth/"   ## Change temp_dep into "./"    ####################
temp_csv = "/Volumes/MyPassport1/" + args.day + "/CSV/"     ## Change temp_csv into "./"    ####################
temp_day = "./outputs/" + args.day + "/" + args.day + "_"   


for cowid in os.listdir(temp_dep):
  summ = os.path.join(temp_day+cowid+".csv")
  if os.path.isfile(summ):
    print("already there, go to next one")
    continue
  else:
      depthdir = temp_dep + cowid + "/"
      csvdir = temp_csv + cowid + "/"
      # print(depthdir)
      with open(summ, "w", newline = "") as output:
          writer = csv.writer(output)
          writer.writerow(["Day", "ID", "Frame", "Width", "Length", "Height_Centroid", "Height_average", "Volume"])
          for root, dirs, files in os.walk(depthdir):
            Day = root.split("/")[3]                  ## If run for github, change [3] into [2] ###################      
            ID = root.split("/")[5]                   ## If run for github, change [5] into [4] ###################
            for file in files:
                file_path = os.path.join(root, file)
                print("Now is running: ", file_path)
                if file_path == "/Volumes/MyPassport1/D14/depth/5724PM/_Depth_198.png":
                  continue
                img = cv2.imread(file_path)
                filename = os.path.splitext(file)[0]+".csv"
                # print(filename)
                csv_path = os.path.join(csvdir, filename)
                dfcsv = pd.read_csv(csv_path, header = None) #read in depth csv file
                dfcsv_crop = dfcsv.iloc[140:390, 120:750]

                img_crop = img[140:390, 120:750]
                hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)
                hue = hsv[:, :, 0] 
                for thresh in range(30,46):
                  # print(thresh0)
                  thresh, thresh_img = cv2.threshold(hue, thresh, 255, cv2.THRESH_BINARY)
                  cnts, _ = cv2.findContours(thresh_img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 
                      # print(f"There are {len(cnts)} countorus (shapes) in total \n")
                  cmax = max(cnts, key=cv2.contourArea) 
                  mask = np.zeros(thresh_img.shape, dtype = thresh_img.dtype) 
                  fill_img = cv2.drawContours(mask, [cmax], 0, (255), -1) 


                  x,y,w,hh = cv2.boundingRect(cmax)
                      # QC for touching boundires
                  frame = os.path.splitext(file)[0]
                  width = np.nan
                  length = np.nan
                  height0 = np.nan 
                  height1 = np.nan 
                  volume = np.nan
                  if (y <= 0 or y+hh >= 250 or x <= 0): 
                      continue
                  else: #use this hue threshold
                    print("threshold is: ", thresh)
                    print("x, y, y+h are:", x, y, y+hh, "\n")


                      ##part0. Neck removing
                    neck_threshold = 0.4 # Neck threshold (cols with this number or less white pixels is classified as neck)
                    white_part = np.sum(fill_img, axis=0) / 255
                    neck_cols = (white_part/np.max(white_part) < neck_threshold) # all columns where less then some threshold of white pixels
                    deleted_cols = np.where(neck_cols)[0]
                    deleted_mask = ~(deleted_cols > fill_img.shape[1] / 2) # make sure that we keep the cols on the butt end
                    deleted_cols = np.delete(deleted_cols, deleted_mask) # remove those cols from deletion
                    
                    if deleted_cols.shape[0] != 0:
                        print(f"Neck will be removed with ratio {neck_threshold} \n")
                        fill_img_crop = fill_img[:,0:deleted_cols[0]] # delete the neck cols
                        black_cols = np.zeros_like(fill_img[:, deleted_cols[0]+1:])
                        fill_img = np.concatenate((fill_img_crop, black_cols), axis = 1)

                    else: 
                      print("Neck will be kept \n")
                      fill_img = fill_img
                    # rgb_img = cv2.cvtColor(fill_img, cv2.COLOR_GRAY2RGB)  #############comment out###############
                    # cnts_img_bi = cv2.drawContours(rgb_img.copy(), [cmax], 0, (255,0,255), 3) #############comment out###############
                    # t=cv2.rectangle(cnts_img_bi, (x,y), (x+w,y+hh), (0,255,0), 2) #############comment out###############
                    # cv2.imwrite(img_out + cowid + filename + ".png", t) #############comment out###############

                      ##part1: calculate width and length
                    cnts, _ = cv2.findContours(fill_img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 
                    cmax = max(cnts, key=cv2.contourArea)
                    rect = cv2.minAreaRect(cmax)
                    box = cv2.boxPoints(rect)
                    (A, B, C, D) = np.int0(box)
                    d0 = dist.euclidean(B, C)
                    d1 = dist.euclidean(A, B)
                    width = min(d0, d1)
                    length = max(d0, d1)

                      ##part2: calculated height: centroid method
                    M = cv2.moments(cmax)
                    row_centroid = int(M["m01"] / M["m00"])
                    col_centroid  = int(M["m10"] / M["m00"])
                    height0 = 2.94 - dfcsv_crop.iloc[row_centroid , col_centroid]

                      ##part3: calculate height: average method
                    pixel = np.argwhere(fill_img == 255) #find pixels for white part
                    dfcsv_rows = [] #combine pixel and distance 
                    for row, col in pixel:
                      dfcsv_rows.append([row, col, dfcsv_crop.iloc[row, col]])
                    df = pd.DataFrame(dfcsv_rows, columns = ['row', 'col', 'dist'])

                    df.dist.replace(to_replace=0, value = df.dist.mean(), inplace=True) #replace 0 with average distance
                    height1 = 2.94 - df.dist.mean()

                      ##part4: calculate volume
                    df["height"] = 2.94 - df["dist"] #build new column named height
                    volume = sum(df.height)

                      ##part5: write into csv file.
                    frame = os.path.splitext(file)[0]
                    writer.writerow([Day, ID, frame, width, length, height0, height1, volume])          
                    break
