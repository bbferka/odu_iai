#!/bin/bash

for dirname in $( ls -d */ ); do
    echo item: $dirname
    cd $dirname
    
    python ../createPCD.py
    cd ../
done
