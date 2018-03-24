#!/bin/bash

for filename in $(ls); do
    if [ -f "$filename" ] && [ $(head -c 4 "$filename") != "%PDF" ]; then
        no_ext=$(basename "$filename" | cut -d. -f1)
        convert "$filename" "$no_ext_converted.pdf"
    fi 
done
