# Should wait for a few hours to finish the process.

for f in * ; do
    tar -xf "$f" "${f:0:2}"
    for protein in */*; do
        mv $protein . 
    done
    rm -rf "${f:0:2}" "$f"
done
