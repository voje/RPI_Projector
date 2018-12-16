#!/bin/bash

# build the files
npm run build

flaskdir="../slideshowplus/flask_app"
tmpdir=$(pwd)
cd "${flaskdir}/static"
for d in *; do
    cd "${d}"
        for f in *; do
            if [[ "${#f}" -gt 25 ]]; then
                echo "removing: ${f}"
                rm "${f}"
            fi
        done
    cd ..
done

cd "${tmpdir}"
cp dist/index.html "${flaskdir}"/templates/remote_vue.html
cp dist/static/css/* "${flaskdir}"/static/css/
cp dist/static/js/* "${flaskdir}"/static/js/

echo "Done."

