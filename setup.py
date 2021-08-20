from setuptools import setup
import os

with open("description.md", "r") as fh:
    long_description = fh.read()

version_file = open('VERSION')
version = version_file.read().strip()

setup(name='hlbpy',
      version=version,
      description='high level blender stuff',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Tobias Lemke',
      url="",
      packages=['hlbpy'],
      install_requires=[],
      classifiers=[])

