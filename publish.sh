#!/bin/bash

set -x
set -e

# Build and upload source and wheel on pypi.org
rm -fr dist/
poetry build
poetry publish
