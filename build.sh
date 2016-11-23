#!/bin/bash

BASE_PATH=$(dirname $0)

. $BASE_PATH/common.sh

$BASE_PATH/clone-packages.sh
$BASE_PATH/clone-extra-packages.sh

rm -rf deb logs installed
mkdir installed

for pkg in $PACKAGES; do
  ./debian-packages/build.py --install-deps $pkg
  sudo dpkg -i ./deb/*.deb
  mv ./deb/*.deb ./installed/
done

for pkg in $EXTRA_PACKAGES; do
  ./debian-packages/build.py --install-deps $pkg
  sudo dpkg -i ./deb/*.deb
  mv ./deb/*.deb ./installed/
done

