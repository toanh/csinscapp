import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csinscapp",
    version="0.0.4",
    author="Toan Huynh",
    author_email="toan@csinschools.io",
    description="A simple UI library wrapping the REMI library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toanh/csinscapp",
    packages=setuptools.find_packages(),
    install_requires=[
              'remi>=2020.3.10',
          ],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
