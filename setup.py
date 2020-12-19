from distutils.core import setup
import py2exe

setup(console=['pcMenu2.py'], requires=['tabulate', 'termcolor'])