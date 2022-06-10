#from re import M
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from matplotlib.widgets import Slider, Button

#view = 'cor' #need to change this to argparse

def view_slices(mri_shape, mri_data, view):
    plt.style.use('dark_background')
    plt.subplots_adjust(left=0.25, bottom=0.25)

    if view == 'sag':
        max_slice = mri_shape[0]
        mid_slice = mri_shape[0]//2
        l = plt.imshow(mri_data[mid_slice, :, :].T, cmap='gray', origin='lower')
        slabel = 'Sagittal slices '
        
    if view == 'cor':
        max_slice = mri_shape[1]
        mid_slice = mri_shape[1]//2
        l = plt.imshow(mri_data[:, mid_slice, :].T, cmap='gray', origin='lower')
        slabel = 'Coronal slices '
        
    if view == 'axi':
        max_slice = mri_shape[2]
        mid_slice = mri_shape[2]//2
        l = plt.imshow(mri_data[:, :, mid_slice].T, cmap='gray', origin='lower')
        slabel = 'Axial slices '
        
    plt.axis('off')
    axislice = plt.axes([0.25, 0.1, 0.65, 0.03])
    sslice=Slider(ax=axislice, 
        label=slabel, 
        valmin=0, 
        valmax=max_slice-1, 
        valstep=1, 
        valinit=mid_slice)


    def update(val):
        slice=np.around(sslice.val)
        if view == 'sag':
            l.set_data(mri_data[slice, :, :].T)
        if view == 'cor':
            l.set_data(mri_data[:, slice, :].T)
        if view == 'axi':
            l.set_data(mri_data[:, :, slice].T)

    sslice.on_changed(update)
    plt.show()


def multi_view(mri_shape, mri_data):

    max_slice_sag = mri_shape[0]
    max_slice_cor = mri_shape[1]
    max_slice_axi = mri_shape[2]
    mid_slice_sag = mri_shape[0]//2
    mid_slice_cor = mri_shape[1]//2
    mid_slice_axi = mri_shape[2]//2
    sag_mid = mri_data[mri_shape[0]//2, :, :]
    cor_mid = mri_data[:, mri_shape[1]//2, :]
    axi_mid = mri_data[:, :, mri_shape[2]//2]

    #slices = [sag_mid, cor_mid, axi_mid]
    plt.style.use('dark_background')
    fig, axes = plt.subplots(1,3)
    l_sag = axes[0].imshow(sag_mid.T, cmap='gray', origin='lower')
    l_cor = axes[1].imshow(cor_mid.T, cmap='gray', origin='lower')
    l_axi = axes[2].imshow(axi_mid.T, cmap='gray', origin='lower')
    axes[0].axis('off')
    axes[1].axis('off')
    axes[2].axis('off')

    # sagittal
    axislice_sag = plt.axes([0.25, 0.1, 0.65, 0.03])
    sslice_sag=Slider(ax=axislice_sag, 
        label='Sagittal slices ', 
        valmin=0, 
        valmax=max_slice_sag-1, 
        valstep=1, 
        valinit=mid_slice_sag)
    
    def update_sag(val):
        slice=np.around(sslice_sag.val)
        l_sag.set_data(mri_data[slice, :, :].T)


    sslice_sag.on_changed(update_sag)

    # coronal
    axislice_cor = plt.axes([0.25, 0.06, 0.65, 0.03])
    sslice_cor=Slider(ax=axislice_cor, 
        label='Coronal slices ', 
        valmin=0, 
        valmax=max_slice_cor-1, 
        valstep=1, 
        valinit=mid_slice_cor)
    
    def update_cor(val):
        slice=np.around(sslice_cor.val)
        l_cor.set_data(mri_data[:, slice, :].T)


    sslice_cor.on_changed(update_cor)

    # axial
    axislice_axi = plt.axes([0.25, 0.02, 0.65, 0.03])
    sslice_axi=Slider(ax=axislice_axi, 
        label='Axial slices ', 
        valmin=0, 
        valmax=max_slice_axi-1, 
        valstep=1, 
        valinit=mid_slice_axi)
    
    def update_axi(val):
        slice=np.around(sslice_axi.val)
        l_axi.set_data(mri_data[:, :, slice].T)


    sslice_axi.on_changed(update_axi)

    plt.show()


    