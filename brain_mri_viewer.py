#from re import M
import numpy as np
import argparse
import os
import sys
import matplotlib.pyplot as plt
import nibabel as nib
from matplotlib.widgets import Slider, Button
from view_slices import *

def extract_info(mri):
    mri_header = mri.header
    mri_affine = mri.affine
    mri_coord = nib.aff2axcodes(mri_affine)
    x, y, z = mri_coord
    mri_data = mri.get_fdata()
    return mri_header, mri_affine, mri_coord, mri_data

def check_coord(mri_coord, mri_data):
    # types of coordinate systems: RAS, LAS, LSA, ALS, RSP, LPS, LIP
    if mri_coord == ('L', 'I', 'P'):
        mri_data = np.flip(mri_data, axis=0) # change L to R (RIP)
        mri_data = np.flip(mri_data, axis=1) # change I to S (RSP)
        mri_data = np.flip(mri_data, axis=2) # change P to A (RSA)
        mri_data = np.swapaxes(mri_data, 1, 2) # swap S and A (RAS)

    # NEED TO CHECK
    if mri_coord == ('L', 'A', 'S'):
        mri_data = np.flip(mri_data, axis=0) # change L to R (RAS) 

    # NEED TO CHECK
    if mri_coord == ('L', 'S', 'A'):
        mri_data = np.flip(mri_data, axis=0) # change L to R (RSA) 
        mri_data = np.swapaxes(mri_data, 1, 2) # swap S and A (RAS)
    
    # NEED TO CHECK
    if mri_coord == ('A', 'L', 'S'):
        mri_data = np.flip(mri_data, axis=1) # change L to R (ARS)
        mri_data = np.swapaxes(mri_data, 0, 1) # swap A nad L (RAS)
    
    # NEED TO CHECK
    if mri_coord == ('R', 'S', 'P'):
        mri_data = np.flip(mri_data, axis=2) # change P to A (RSA)
        mri_data = np.swapaxes(mri_data, 1, 2) # swap S nad P (RAS)
    
    # NEED TO CHECK
    if mri_coord == ('L', 'P', 'S'):
        mri_data = np.flip(mri_data, axis=0) # change L to R (RPS)
        mri_data = np.flip(mri_data, axis=1) # change P to A (RAS)

    mri_shape = np.asarray(mri_data.shape)

    return mri_data, mri_shape

def display_info(mri_header, mri_affine, mri_coord, mri_data):
    # Display MRI general info
    print("""
    ############################
    #### MRI Math Windowing ####
    ############################""")
    print("\n")
    print('MRI header\n', mri_header) 
    print("\n")
    print('MRI affine\n', mri_affine)
    print("\n")
    print('MRI coordinate system\n', mri_coord)
    print("\n")
    #print('MRI data\n', mri_1_data)
    # print("\n")
    print('MRI data type: ', type(mri_data))
    print('MRI dtype: ', mri_data.dtype)
    print('min voxel intensity: ', np.min(mri_data))
    print('max voxel intensity: ', np.max(mri_data))
    print('MRI shape: ', mri_data.shape)
    print('MRI dim: ', mri_data.ndim)

def visualize_img(mri_data, mri_shape):
    # Visualizing MRI's mid slices

    sag_mid = mri_data[mri_shape[0]//2, :, :]
    cor_mid = mri_data[:, mri_shape[1]//2, :]
    axi_mid = mri_data[:, :, mri_shape[2]//2]

    slices = [sag_mid, cor_mid, axi_mid]
    plt.style.use('dark_background')
    fig, axes = plt.subplots(1,len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap='gray', origin='lower')
        axes[i].axis('off')

    axes[0].set_title('Sagittal view')
    axes[1].set_title('Coronal view')
    axes[2].set_title('Axial view')
    plt.show()
    return

def main():
    parser = argparse.ArgumentParser(description=' ################ Brain MRI Viewer ################', usage='%(prog)s [--input] [options]')
    parser.add_argument('-in', '--input', type=str, required=True, help='MRIs file path', dest='in_path')
    parser.add_argument('-v', '--view', type=str, choices=['multiview', 'sag', 'cor', 'axi'], default='multiview', dest='view', help='select view [sag, cor, axi, multiview]')
    parser.add_argument('-img', '--image', action='store_true', dest='img', help='shows MRIs image')
    # add volume option
    args = parser.parse_args()

    mri = nib.load(args.in_path)
    view = args.view

    mri_header, mri_affine, mri_coord, mri_data = extract_info(mri)
    display_info(mri_header, mri_affine, mri_coord, mri_data)
    mri_data, mri_shape = check_coord(mri_coord, mri_data)

    if args.img == True:
        visualize_img(mri_data, mri_shape)
    elif args.view != 'multiview':
        view_slices(mri_shape, mri_data, view) # in the future add string 'sag' 'cor' 'axi' w/ arparse
    else:
        multi_view(mri_shape, mri_data)


if __name__ == "__main__":
    main()