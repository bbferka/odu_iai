#/bin/bash
# batch rename files in folders by replacing user given string with folder name
# Usage: copy script into folder wher you want to run it 


for d in */ ; do
    echo "$d"
    cd $d
    ls | grep 30_0_crop.png
    echo -n "Enter name to replace and press [ENTER]: "
    read name
    replacment="s\/${d}\/${name}\/g"
    export name_to_replace=${name}
    export name_to_replace_with=${d%?} 
    rename -v 's/\Q$ENV{name_to_replace}\E/$ENV{name_to_replace_with}/' ./* 
    cd ..
done
