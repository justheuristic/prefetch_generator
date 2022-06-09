from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

import prefetch_generator
# loading README
long_description = prefetch_generator.__doc__

version_string = '1.0.2'

setup(
    name="prefetch_generator",
    version=version_string,
    description="a simple tool to compute arbitrary generator in a background thread",
    long_description=long_description,

    # Author details
    author_email="justheuristic@gmail.com",
    url="https://github.com/justheuristic/prefetch_generator",

    # Choose your license
    license='The Unlicense',
    packages=find_packages(),

    classifiers=[
        # Indicate who your project is intended for
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: The Unlicense (Unlicense)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

    ],

    # What does your project relate to?
    keywords='background generator, prefetch generator, parallel generator, prefetch, background,' + \
             'deep learning, theano, tensorflow, lasagne, blocks',

    # List run-time dependencies here. These will be installed by pip when your project is installed.
    install_requires=[
        #nothing
    ],
)
