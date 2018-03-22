#!/bin/bash

for filename in $(ls); do
    if [ -f "$filename" ] && [ $(head -c 4 "$filename") != "%PDF" ]; then
        no_ext=$(basename "$filename" | cut -d. -f1)
        convert "$filename" "converted_$no_ext.pdf"
    fi 
done
