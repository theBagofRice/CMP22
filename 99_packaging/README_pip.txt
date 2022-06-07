Steps for packaging with PIP:


There are many ways to package and to customize. See websites
listed below for more information. Here are some basic steps.


1) Create an empty directory and place a file 'setup.py' into it

The file 'setup.py' must contain a call to the function 'setup' which
has been imported from setuptools. Setuptools as a library that allows
you to package a project. The function setup has many possible arguments.
Most importantly it needs the location of the source code - provided in the
example here by the function 'find_packages' which will scan through all
subdirectories and return python packages (.py files) it found.
Additionally the function setup can be used to specify various meta data
like version, author, dependencies etc. 


2) Create a subdirectory containing the source code. 

In the present case the subdirectory is called 'cmp22' and it contains
the file 'functions.py' that holds the functions f1 to f6 from problem 3.
The name cmp22 will be the name to use in the 'import' statement. 
a file 'VERSION' that contains the current version number and a file
'__init__.py'.

In '__init__.py' one can perform operations that need to be done to
make the package functional (like loading data files etc.). Here
just the functions are imported. 


3) Install the package with 

 pip install [-e] .

(note the dot '.') The -e option installs a link to the the current directory.
Without the -e options the files are copied into your installation.
If a link is installed, changes in the source files will become available
intermediately and no re-install is needed.


4) Create a package file

Alternatively one can also create a package file that contains all the
source and meta data (essentially it is a .zip file of the package
directory - try to unzip and take a look.)

 python setup.py bdist_wheel --universal

This will create among others a directory 'dist' containing a package file,
here  cmp22-0.1.0-py2.py3-none-any.whl

This file can also be installed with PIP:

 pip install  dist/cmp22-0.1.0-py2.py3-none-any.whl



See also:

https://packaging.python.org/tutorials/packaging-projects/

https://packaging.python.org/en/latest/tutorials/installing-packages/

https://www.realpythonproject.com/how-to-create-a-wheel-file-for-your-python-package-and-import-it-in-another-project/


