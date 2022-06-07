from setuptools import setup, find_packages

import os



version_file = open(os.path.join("./cmp22", 'VERSION'))
version = version_file.read().strip()

setup(
    name='cmp22',
    version=version, 
    description='CMP 22 source files',
    author='Markus Schroeder',
    author_email='markus.schroeder@pci.uni-heidelberg.de',
    license='None',
    packages=find_packages(),
    install_requires=['scipy',
                      'numpy'],
)

