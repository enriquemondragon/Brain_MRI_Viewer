Brain MRI Viewer
===============

**MRI viewer and windowing tool.**

The motivation behind this project was to implement MRI preprocessing, visualization and windowing from scratch.

With this code you can:
- Visualize the slices of each view (sagittal, coronal and axial) of your MRI NIfTi file (3 or 4 dimensions)
- Apply windowing to the MRI by managing the window width and level

--------
## Project setup

You can clone the repository by using the command:

```
    $ git clone https://github.com/enriquemondragon/Brain_MRI_Viewer.git
```

Then, in the project's folder, you can execute the Makefile to setup the project and activate the created environment:

```
    $ make
    $ source venv/bin/activate
```
--------
## Usage
By default when loading an MRI, you will be able to visualize all three views at the same time

```
    python3 brain_mri_viewer.py --input [NifTi_file]
```

![Multiview](/images/multiview.png)

If you want to see only 1 view at a time, yo can specify it with the view flag

```
    python3 brain_mri_viewer.py --input [NifTi_file] --view {sag, cor, axi}
```

![single view](/images/cor_view.png)

For applying windowing you can use the window flag in either cases

```
    python3 brain_mri_viewer.py --input [NifTi_file] --window
```

![WIndowing](/images/windowing.png)

--------
## Author
Name: Enrique Mondragon Estrada

Mail: emondra99@gmail.com

--------
## Sources
Documentation that was useful when writing the code and can be use for further develop

- FreeSurferWiki - Free Surfer Wiki. (2022). FreeSurfer. https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferWiki
- Neuroimaging in Python — NiBabel 4.0.0rc0+1.g1e71f453 documentation. (n.d.). NiBabel. https://nipy.org/nibabel/
- Rodríguez, V. (2019). Medical Images In python (Computed Tomography). Vincentblog. https://vincentblog.xyz/posts/medical-images-in-python-computed-tomography
- Zhao, X., Zhang, T., Liu, H., Zhu, G., & Zou, X. (2019). Automatic Windowing for MRI With Convolutional Neural Network. IEEE Access, 7, 68594–68606. https://doi.org/10.1109/access.2019.2918814


--------
## License
Brain MRI Viewer is available under the MIT license. See the LICENSE file for more info.