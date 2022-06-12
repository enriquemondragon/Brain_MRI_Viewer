# Brain MRI Viewer

**MRI viewer and windowing tool.**

You can:
- Visualize the slices of each view (sagittal, coronal and axial) of your MRI NIfTi file (3 or 4 dimensions)
- Apply windowing to the MRI by managing the window width and level

--------
## Usage
BY default when loading a MRI, you will be able to visualize all three views at the same time

```
    python3 brain_mri_viewer.py --input [NifTi_file]
```

![Multiview](/images/multiview.png)

In you want to see only 1 view at a time, yo can specify it with the view flag

```
    python3 brain_mri_viewer.py --input [NifTi_file] --view {sag, cor, axi}
```

![single view](/images/cor_view.png)

For applying windowing use the window flag in either cases

```
    python3 brain_mri_viewer.py --input [NifTi_file] --window
```

![WIndowing](/images/windowing.png)