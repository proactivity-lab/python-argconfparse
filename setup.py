"""
argconfparse: Python argparse with options to read argument values from configuration files.
With argconfparse it is possible to provide a configuration file from where argument values are read.
Command-line values override values in the provided configuration file.
"""

from setuptools import setup

doclines = __doc__.split("\n")

setup(name='argconfparse',
      version='0.1.1',
      description='Python argparse with options to read argument values from configuration files.',
      long_description='\n'.join(doclines[2:]),
      url='http://github.com/proactivity-lab/python-argconfparse',
      author='Raido Pahtma',
      author_email='raido.pahtma@ttu.ee',
      license='MIT',
      platforms=["any"],
      packages=['argconfparse'],
      zip_safe=False)
