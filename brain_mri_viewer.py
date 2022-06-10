#from re import M
from re import M
import numpy as np
import argparse
import os
import sys
import matplotlib.pyplot as plt
import nibabel as nib
from matplotlib.widgets import Slider, Button
from view_slices import *

def extract_info(mri):
    ''' 
    Extract general information from MRI 

    Arguments: 
    mri -- MRI NifTi file

    Returns:
    mri_header --contains general information from the MRI
    mri_affine -- affine matrix
    mri_coord -- MRI coordinate system
    mri_data --  MRI array
    '''
    mri_header = mri.header
    mri_affine = mri.affine
    mri_coord = nib.aff2axcodes(mri_affine)
    x, y, z = mri_coord
    mri_data = mri.get_fdata()
    return mri_header, mri_affine, mri_coord, mri_data


def check_coord(mri_coord, mri_data):
    ''' 
    Check the MRI's coordinate system and transforms it to RAS in case it is other

    Arguments: 
    mri_coord -- MRI coordinate system
    mri_data --  MRI array

    Returns:
    mri_data --  MRI array transformed to RAS coordinate system
    mri_shape -- shape of the MRI array in RAS coordinate system

    Note: types of coordinate systems that check: RAS, LAS, LSA, ALS, RSP, LPS, LIP
    '''
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
    ''' 
    Display general information from the MRI

    Arguments: 
    mri_header --contains general information from the MRI
    mri_affine -- affine matrix
    mri_coord -- MRI coordinate system
    mri_data --  MRI array
    '''
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
    # print('MRI data\n', mri_data)
    # print("\n")
    print('MRI data type: ', type(mri_data))
    print('MRI dtype: ', mri_data.dtype)
    print('min voxel intensity: ', np.min(mri_data))
    print('max voxel intensity: ', np.max(mri_data))
    print('MRI shape: ', mri_data.shape)
    print('MRI dim: ', mri_data.ndim)


def visualize_img(mri_data, mri_shape):
    '''
    Outputs an image of the mid slices of the MRI in each view (sagittal, coronal and axial)

    Arguments:
    mri_data --  MRI array
    mri_shape -- shape of the MRI array
    '''

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
    parser.add_argument('-w', '--window', action='store_true', dest='window', help='enables the option for MRI windowing')
    # add volume option
    args = parser.parse_args()

    mri = nib.load(args.in_path)
    view = args.view 

    mri_header, mri_affine, mri_coord, mri_data = extract_info(mri)
    display_info(mri_header, mri_affine, mri_coord, mri_data)
    mri_data, mri_shape = check_coord(mri_coord, mri_data)

    if args.window and args.img == False:
        print("\n")
        print('MRI slope: ', mri.dataobj.slope) 
        print('MRI interception: ', mri.dataobj.inter)

        def rescale(a ,x, b):
            return a * x + b


        def hounsfield(mri, mri_data):
            '''
            Transforms MRI to Hounsfield units (HU) by rescaling it

            Arguments:
            mri -- MRI NifTi file
            mri_data --  MRI array

            Returns:
            mri_hu -- MRI converted to HU
            '''
            intercept = mri.dataobj.inter
            slope = mri.dataobj.slope
            mri_hu = rescale(mri_data, slope, intercept)
            return mri_hu


        mri_hu = hounsfield(mri, mri_data)
        if args.view != 'multiview':
            view_slices_window(mri_shape, mri_hu, view)
        else:
            multi_view_window(mri_shape, mri_hu)
    else:
        if args.img:
            visualize_img(mri_data, mri_shape)
        elif args.view != 'multiview':
            view_slices(mri_shape, mri_data, view)
        else:
            multi_view(mri_shape, mri_data)


if __name__ == "__main__":
    main()