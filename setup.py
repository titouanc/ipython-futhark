#!/usr/bin/env python

from setuptools import setup, find_packages

version = '1.1.1'
packages = find_packages()
print(packages)

setup(
    # Metadata
    name='ipython-futhark',
    version=version,
    description="Futhark language embedding into IPython",
    long_description_markdown_filename='README.md',
    keywords='futhark ipython gpu',
    author='Titouan Christophe',
    author_email='moiandme@gmail.com',
    url='https://github.com/titouanc/ipython-futhark',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Framework :: IPython',
        'Framework :: Jupyter'
    ],

    # Package data
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['README.md', 'Demo.ipynb']},
    zip_safe=True,

    # Dependencies
    setup_requires=['setuptools-markdown'],
    install_requires=['numpy', 'ipython'],
    extras_require={'opencl': ['pyopencl']}
)
