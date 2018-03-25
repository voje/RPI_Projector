#!/bin/bash
# use absolute full paths!

default_dir="$(pwd .)/diapozitivi"
indir="${1:-${default_dir}}"
dname=$(dirname "$indir")
bname=$(basename "$indir")
dest_dir="${dname}/pdf_${bname}"
mkdir "${dest_dir}"

cd "${indir}"

for filename in $(ls); do
    if [ -f "$filename" ]; then
        if [ $(head -c 4 "${filename}") != "%PDF" ]; then
            no_ext=$(basename "${filename}" | cut -d. -f1)
            new_path="${dest_dir}/${no_ext}_c.pdf"
            convert "$filename" "${new_path}"
        else
            cp "${filename}" "${dest_dir}/${filename}"
        fi
    fi
done
