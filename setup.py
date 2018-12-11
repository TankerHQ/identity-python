import sys
from setuptools import setup, find_packages

def get_long_description():
    with open("README.rst") as file:
        return file.read()

setup(name="tankersdk-user-token",
      version="0.3",
      description="Tanker user token library",
      long_description=get_long_description(),
      url="https://github.com/TankerHQ/user-token-python",
      author="Kontrol SAS",
      packages=find_packages(),
      install_requires=["PyNaCl"],
      extras_require={
            "dev": ["pytest"],
      },
      classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
      ],
      )
