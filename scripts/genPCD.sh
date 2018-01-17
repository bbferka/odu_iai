#!/bin/bash

dirname = $1
echo $dirname
#cd $dirname

for dir in $( ls -d */ ); do
    echo item: $dir
    cd $dir
    
#    python ../createPCD.py
    cd ../
done
