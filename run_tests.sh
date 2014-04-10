#!/bin/bash -e

BASE_DIR=`dirname "$0"`

set -x

flake8 --exclude=.tox "${BASE_DIR}"
pep257 generate-inventory.py
