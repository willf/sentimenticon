import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='Sentimenticon',
      version="0.0.1",
      author="Will Fitzgerald",
      author_email="will.fitzgerald@pobox.com",
      description="Word-based sentiment analyzer",
      url='http://github.com/willf/sentimenticon',
      license="BSD",
      keywords="nlp sentiment",
      long_description=read("README.md"),
      packages=find_packages(),
      package_data={'': ['*.txt']})