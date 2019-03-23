# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 11:55:52 2018

@author: meser

fes_gamma_test.py - Initial test of the DPCN front end system gamma kernel
concept in Python. This script applys the gamma kernel saliency model to single
images.

"""

# Standard Library Imports
import time

# 3P Imports
import numpy as np
import matplotlib.pyplot as plt
import scipy.io

# Local Imports
import fes_gamma as fg

plt.rcParams.update({'font.size': 22})


# Main Routine
if __name__ == '__main__':
    plt.close('all')

    # Open test images as 8-bit RGB values - Time ~0.0778813
#    mario = fg.imageObject('./ICASSP Ryan/', 'mario', '.png', RGB=True)
    mario = fg.imageObject('./', 'SMW_Test_Image', '.png', rgb=True)
    banana = fg.imageObject('./AIM/eyetrackingdata/original_images/',
                            '22', '.jpg', rgb=True)
    corner = fg.imageObject('./AIM/eyetrackingdata/original_images/',
                            '120', '.jpg', rgb=True)

    testIMG = mario

    # Convert image to CIELAB Color Space
    testIMG.image_convert()

# %% Generate Saliency Map

    # Generate Gaussian Blur Prior - Time ~0.0020006
    prior = fg.matlab_style_gauss2D(testIMG.modified.shape, sigma=300) * 1

#    mat = scipy.io.loadmat('./ICASSP Ryan/prior.mat')
#    prior = mat['p1']

    # Generate Saliency Map with Gamma Filter
    start = time.time()
    fg.front_end_convolution(testIMG, prior)
    stop = time.time()
    print("Salience Map Generation: ", stop - start, " seconds")

    # Bound and Rank the most Salient Regions of Saliency Map
    fg.salScan2(testIMG, rankCount=4)

# %% Plot Results

    # Plot Bounding Box Patches
    testIMG.draw_image_patches()
    testIMG.plot_saliency_map()

    # Create a figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title('Original')
    ax2.set_title('Saliency Map')
    if (testIMG.rgb):
        ax1.imshow(testIMG.patched)
    else:
        testIMG.modified.astype(int)
        ax1.imshow(testIMG.modified)
    ax2.imshow(testIMG.salience_map)
    plt.show()