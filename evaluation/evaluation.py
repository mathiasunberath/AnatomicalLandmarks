# This code is used for evlauating the landmark prediction result
# Copyright: Cong Gao, the Johns Hopkins University email: cgao11@jhu.edu
import os
import numpy as np
from PIL import Image
import glob

# Original heatmap window size (615, 479)
w_p = 615
h_p = 479
pixel_size = 0.616
# Network prediction heatmap window size (76, 59)
w_hm = 76
h_hm = 59

def criterion_ld(ind, pred, target):
    pred = np.array(pred)
    # Find the maximum response coordinate
    [u1_pre, v1_pre] = np.where(pred == pred.max())
    # Resize back to original dimension
    u1_pre = u1_pre[0] * h_p / h_hm * pixel_size
    v1_pre = v1_pre[0] * w_p / w_hm * pixel_size
    u1_tar = target[1] * pixel_size
    v1_tar = target[0] * pixel_size
    # Calculate l2 distance loss
    loss = np.sqrt(np.square(u1_pre-u1_tar)+np.square(v1_pre-v1_tar))

    return loss

testing_pre_path = './Heatmaps_exp'
testing_pre_pathes = []
for filename_hm in sorted(glob.glob(testing_pre_path+'/*.tif')):
    testing_pre_pathes.append(filename_hm)

loss = []
ind = 0
count = 0
# We set the belief map threshold to be 0.4
threshold = 0.4
with open('groundTruthPoints.txt', "r+") as f:
    data = f.readlines()
    for line in data:
        number = line.strip().split(" ")
        # Initialize prediction heatmap
        pre = np.zeros((h_hm, w_hm))
        # Loop over 6 stages
        for stage in range(0, 6):
            pre_stage = Image.open(testing_pre_pathes[ind*6+stage])
            pre += np.array(pre_stage)
        # Avereage across the 6 stage prediction
        pre = pre/6
        grd = [float(number[0]), float(number[1])]
        if pre.max() >= threshold:
            count += 1
            current_loss = criterion_ld(ind, pre, grd)
            loss.append(current_loss)
        ind += 1

print('Landmark count:', count, 'Mean:', np.mean(loss), 'STD:', np.std(loss))
