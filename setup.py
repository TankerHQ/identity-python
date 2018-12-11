import sys
from setuptools import setup, find_packages

setup(name="tankersdk-user-token",
      version="0.3",
      description="Tanker user token library",
      long_description="Building blocks to create your own user token server to use with the Tanker SDK",
      url="https://github.com/TankerHQ/user-token-python",
      author="Kontrol SAS",
      packages=find_packages(),
      install_requires=["PyNaCl"],
      classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
      ],
      )
