#!/bin/bash
find `pwd` -maxdepth 2 -type f -iname "*.obj" -exec rosrun interface cmd_line_generate_sift_model {} \;
