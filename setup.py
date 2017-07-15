from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


version = '1.0.0'

setup(
    name='ipython-futhark',
    version=version,
    description="Futhark language embedding into IPython",
    long_description=README,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
    ],
    keywords='futhark ipython gpu',
    author='Titouan Christophe',
    author_email='moiandme@gmail.com',
    url='https://pypi.python.org/pypi/ipython-futhark',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=['numpy', 'ipython>=1.0'],
    extras_require={'opencl': ['pyopencl']}
)
