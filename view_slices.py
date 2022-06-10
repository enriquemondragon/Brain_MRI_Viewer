#from re import M
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from matplotlib.widgets import Slider, Button

def view_slices(mri_shape, mri_data, view):
    ''' 
    Outputs a figure where the slices of 1 view (sagittal, coronal or axial) can be viewed 

    Arguments: 
    mri_shape -- shape of the MRI array
    mri_data --  MRI array
    view -- string containing the view to display
    '''
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
    ''' 
    Outputs a figure where the slices of the 3 views (sagittal, coronal or axial) can be viewed 

    Arguments: 
    mri_shape -- shape of the MRI array
    mri_data --  MRI array
    '''
    max_slice_sag = mri_shape[0]
    max_slice_cor = mri_shape[1]
    max_slice_axi = mri_shape[2]
    mid_slice_sag = mri_shape[0]//2
    mid_slice_cor = mri_shape[1]//2
    mid_slice_axi = mri_shape[2]//2
    sag_mid = mri_data[mri_shape[0]//2, :, :]
    cor_mid = mri_data[:, mri_shape[1]//2, :]
    axi_mid = mri_data[:, :, mri_shape[2]//2]

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


def windowing(mri_hu, wl, ww):

    ''' 
    Computes windowing for MRI
    Arguments: 
    mri_hu -- MRI converted to HU
    wl -- window level
    ww -- window width
    Returns:
    mri_window -- MRI with windowing applied
    '''
    min_window = wl - ww // 2
    max_window = wl + ww // 2
    mri_window = mri_hu.copy()
    mri_window [mri_window  < min_window] = min_window
    mri_window [mri_window  > max_window] = max_window
    return mri_window


def view_slices_window(mri_shape, mri_hu, view):
    ''' 
    Outputs a figure where the slices of 1 view (sagittal, coronal or axial) can be viewed and windowing can be applied

    Arguments: 
    mri_shape -- shape of the MRI array
    mri_hu -- MRI converted to HU
    view -- string containing the view to display
    '''
    plt.style.use('dark_background')
    plt.subplots_adjust(left=0.25, bottom=0.25)

    wl_init = 150
    ww_init = 300

    if view == 'sag':
        max_slice = mri_shape[0]
        mid_slice = mri_shape[0]//2
        l = plt.imshow(windowing(mri_hu, wl_init, ww_init)[mid_slice, :, :].T, cmap='gray', origin='lower')
        slabel = 'Sagittal slices '
        
    if view == 'cor':
        max_slice = mri_shape[1]
        mid_slice = mri_shape[1]//2
        l = plt.imshow(windowing(mri_hu, wl_init, ww_init)[:, mid_slice, :].T, cmap='gray', origin='lower')
        slabel = 'Coronal slices '
        
    if view == 'axi':
        max_slice = mri_shape[2]
        mid_slice = mri_shape[2]//2
        l = plt.imshow(windowing(mri_hu, wl_init, ww_init)[:, :, mid_slice].T, cmap='gray', origin='lower')
        slabel = 'Axial slices '
        
    plt.axis('off')
    axislice = plt.axes([0.25, 0.1, 0.65, 0.03])
    sslice=Slider(ax=axislice, 
        label=slabel, 
        valmin=0, 
        valmax=max_slice-1, 
        valstep=1, 
        valinit=mid_slice)

    axiwindow_width = plt.axes([0.1, 0.25, 0.0225, 0.63])
    swidth=Slider(ax=axiwindow_width, 
        label='Window \n width ', 
        valmin=0, 
        valmax=500, 
        valstep=1, 
        valinit=ww_init,
        orientation="vertical")
    
    axiwindow_level = plt.axes([0.2, 0.25, 0.0225, 0.63])
    slevel=Slider(ax=axiwindow_level, 
        label='Window \n level ', 
        valmin=0, 
        valmax=500, 
        valstep=1, 
        valinit=wl_init,
        orientation="vertical")

    def update(val):
        slice=np.around(sslice.val)
        width=np.around(swidth.val)
        level=np.around(slevel.val)
        if view == 'sag':
            l.set_data(windowing(mri_hu, level, width)[slice, :, :].T)
        if view == 'cor':
            l.set_data(windowing(mri_hu, level, width)[:, slice, :].T)
        if view == 'axi':
            l.set_data(windowing(mri_hu, level, width)[:, :, slice].T)


    sslice.on_changed(update)
    swidth.on_changed(update)
    slevel.on_changed(update)

    plt.show()  


def multi_view_window(mri_shape, mri_hu):
    ''' 
    Outputs a figure where the slices of the 3 views (sagittal, coronal or axial) can be viewed 

    Arguments: 
    mri_shape -- shape of the MRI array
    mri_hu -- MRI converted to HU
    '''
    wl_init = 150
    ww_init = 300
    
    max_slice_cor = mri_shape[1]
    max_slice_axi = mri_shape[2]
    mid_slice_sag = mri_shape[0]//2
    mid_slice_cor = mri_shape[1]//2
    max_slice_sag = mri_shape[0]
    mid_slice_axi = mri_shape[2]//2
    sag_mid = windowing(mri_hu, wl_init, ww_init)[mri_shape[0]//2, :, :]
    cor_mid = windowing(mri_hu, wl_init, ww_init)[:, mri_shape[1]//2, :]
    axi_mid = windowing(mri_hu, wl_init, ww_init)[:, :, mri_shape[2]//2]

    plt.style.use('dark_background')
    fig, axes = plt.subplots(1,3)
    l_sag = axes[0].imshow(sag_mid.T, cmap='gray', origin='lower')
    l_cor = axes[1].imshow(cor_mid.T, cmap='gray', origin='lower')
    l_axi = axes[2].imshow(axi_mid.T, cmap='gray', origin='lower')
    axes[0].axis('off')
    axes[1].axis('off')
    axes[2].axis('off')

    axiwindow_width = plt.axes([0.05, 0.25, 0.0225, 0.63])
    swidth=Slider(ax=axiwindow_width, 
        label='Window \n width ', 
        valmin=0, 
        valmax=500, 
        valstep=1, 
        valinit=ww_init,
        orientation="vertical")
    
    axiwindow_level = plt.axes([0.92, 0.25, 0.0225, 0.63])
    slevel=Slider(ax=axiwindow_level, 
        label='Window \n level ', 
        valmin=0, 
        valmax=500, 
        valstep=1, 
        valinit=wl_init,
        orientation="vertical")

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
        width=np.around(swidth.val)
        level=np.around(slevel.val)
        l_sag.set_data(windowing(mri_hu, level, width)[slice, :, :].T)


    sslice_sag.on_changed(update_sag)
    swidth.on_changed(update_sag)
    slevel.on_changed(update_sag)

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
        width=np.around(swidth.val)
        level=np.around(slevel.val)
        l_cor.set_data(windowing(mri_hu, level, width)[:, slice, :].T)


    sslice_cor.on_changed(update_cor)
    swidth.on_changed(update_cor)
    slevel.on_changed(update_cor)

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
        width=np.around(swidth.val)
        level=np.around(slevel.val)
        l_axi.set_data(windowing(mri_hu, level, width)[:, :, slice].T)


    sslice_axi.on_changed(update_axi)
    swidth.on_changed(update_axi)
    slevel.on_changed(update_axi)

    plt.show()