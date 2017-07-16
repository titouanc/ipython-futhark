# ipython-futhark

Embed [Futhark](http://futhark-lang.org) code into your favourite IPython
shells and Notebooks.

## Install

You should have a working version of Futhark in your `$PATH`. To do so, read
the installation instructions on
[readthedocs.io](https://futhark.readthedocs.io/en/latest/installation.html).

Then install ipython-futhark using pip:

* ipython futhark only: `$ pip install ipython-futhark`
* Installing pyopencl along the way: `$ pip install ipython-futhark[opencl]`

## Example

See [the Notebook demo](http://nbviewer.jupyter.org/github/titouanc/ipython-futhark/blob/master/Demo.ipynb)

```ipython
IPython 5.4.1 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: %load_ext futhark

In [2]: %%futhark gpu
   ...: let main(): i32 = 42
   ...: 
Warning: Device limits tile size to 22 (setting was 32)

In [3]: main()
Out[3]: 42

In [4]: %%futhark inspect gpu
   ...: let main(): f32 = 42
   ...: 
In: main(): f32 = 42
Declaration of function main at tmpDWm0Zs.fut:1:5-1:5 declares return type f32, but body has type i32
If you find this error message confusing, uninformative, or wrong, please open an issue at https://github.com/HIPERFIT/futhark/issues.

```
