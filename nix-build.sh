#!/bin/bash

START_DIR=$(pwd)

# update pc files
echo "Update pc files..."
cd installation
python update_pc_files.py

# get a few additional executables needed for the class
echo "\nGet gridgen and triangle..."
get-modflow --subset gridgen,triangle :python

echo "\nGet PEST++..."
get-pestpp :python

# return to starting directory
cd "$START_DIR"

# clone modflow6 repo
echo "\nClone the MODFLOW 6 repo..."
rm -rf modflow6
git clone https://github.com/MODFLOW-USGS/modflow6.git
cd modflow6

# build modflow 6
echo "\nBuild and test MODFLOW 6"
rm -rf builddir
meson setup builddir -Ddebug=false -Dextended=true --prefix=$CONDA_PREFIX/bin/
meson install -C builddir
meson test --verbose --no-rebuild -C builddir

# finish
cd "$START_DIR"
echo "\nFinished...\n\n"


