from setuptools import setup, find_packages


def get_long_description():
    with open("README.rst") as file:
        return file.read()


setup(
    name="tankersdk-identity",
    version="1.2.0",
    description="Tanker identity library",
    long_description=get_long_description(),
    url="https://github.com/TankerHQ/identity-python",
    author="Kontrol SAS",
    packages=find_packages(),
    install_requires=["PyNaCl"],
    extras_require={
        "dev": [
            "codecov",
            "pytest",
            "pytest-cov",
            "twine",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
