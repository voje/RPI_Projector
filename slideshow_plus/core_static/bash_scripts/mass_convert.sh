#!/bin/bash

# Obsolete: using geeqie for displaying images instead of converting to .pdf.
echo "OBSOLETE!"
exit 1

# use absolute full paths!

indir="$(pwd .)/diapozitivi"
indir="${1:-${indir}}"

dname=$(dirname "$indir")
bname=$(basename "$indir")

dest_dir="${dname}/converted_${bname}"
dest_dir="${2:-${dest_dir}}"

# echo "$indir"
# echo "$dest_dir"
# exit 0

mkdir "${dest_dir}"

cd "${indir}"

for filename in $(ls); do
    if [ -f "$filename" ]; then
        if [ $(head -c 4 "${filename}") != "%PDF" ]; then
            no_ext=$(basename "${filename}" | cut -d. -f1)
            new_path="${dest_dir}/${no_ext}.pdf"
            convert "$filename" "${new_path}"
        fi
    fi
done

