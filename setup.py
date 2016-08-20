from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_version():
    with open("rusclasp/version.py", "rt") as f:
        return f.readline().split("=")[1].strip(' "\n')


setup(
    name='losc',
    version=get_version(),
    author='Grigory Ignatyev',
    author_email='ignatyeff.g@gmail.com',
    url='https://github.com/gree-gorey/losc/',

    description='Lists of stimuli creator.',
    long_description=open('README.md').read(),

    license='GNU GENERAL PUBLIC LICENSE',
    packages=[
        'losc'
    ],
    requires=[
        'werkzeug',
        'jinja2',
        'itsdangerous',
        'numpy',
        'scipy',
        'flask'
    ],
    install_requires=[
        'numpy',
        'scipy',
        'flask'
    ],
    package_data={
        # 'rusclasp': ['data/store.p']
    },
    zip_safe=False,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        # 'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # 'Topic :: Scientific/Engineering :: Information Analysis',
        # 'Topic :: Text Processing :: Linguistic',
    ],

    keywords='stimuli',
)
