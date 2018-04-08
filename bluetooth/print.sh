#!/bin/bash

IFS='£' #I want to catch enter and space.

while true; do
    read -s -d '' -n 1 key
    printf ">> %q\n" $key     
done
