#!/bin/bash
rm -R docs/doctrees
mv docs html
cd html
make html
cd ..
mv html docs
mv doctrees docs
