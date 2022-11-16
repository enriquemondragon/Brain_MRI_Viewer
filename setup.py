from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='brain_mri_viewer',
    version='1.0',
    packages=find_packages(include=['brain_mri_viewer', 'brain_mri_viewer.*']),
    license='MIT license',
    author='Enrique Mondragon Estrada',
    author_email='emondra99@gmail.com',
    description='MRI viewer and windowing tool',
    url='https://github.com/enriquemondragon/Brain_MRI_Viewer'
)
