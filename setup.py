# Fix for older setuptools
import re
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    try:
        return open(fpath(fname), encoding='utf8').read()
    except TypeError:  # Python 2's open doesn't have the encoding kwarg
        return open(fpath(fname)).read()


def desc():
    return read('README.md')


# grep flask_simplelogin/__init__.py since python 3.x cannot
# import it before using 2to3
file_text = read(fpath('flask_simplelogin/__init__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    name='flask_simplelogin',
    version=grep('__version__'),
    url='https://github.com/cuducos/flask_simplelogin/',
    license='MIT',
    author=grep('__author__'),
    author_email=grep('__email__'),
    description='Flask Simple Login - Login Extension for Flask',
    long_description=desc(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['Flask>=0.12', 'click', 'flask_wtf']
)
