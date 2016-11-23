#!/bin/bash

. $(dirname $0)/common.sh

for pkg in $PACKAGES; do
  [ -d $pkg ] || git clone https://github.com/mate-desktop/${pkg}.git
  pushd $pkg
  git fetch --tags
  git checkout $(git tag -l | tail -n 1)
  popd
done
