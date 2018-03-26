import sys
from setuptools import setup

if sys.version_info.major < 3:
    sys.exit("Error: Please upgrade to Python3")


setup(name="tankersdk-user-token",
      version="0.2",
      description="Tanker user token library",
      long_description="Building blocks to create your own user token server to use with the Tanker SDK",
      url="https://tanker.io",
      author="Kontrol SAS",
      packages=[
          "tankersdk.crypto",
          "tankersdk.usertoken",
      ],
      install_requires=["PyNaCl"],
      classifiers=[
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
      ],
      )
