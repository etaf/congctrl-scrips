#!/bin/bash

for file_name in `find . -type f -name 'sender*' `; do
    echo "processing $file_name"
    nline=`wc -l $file_name | awk '{ print $1 }'`
    echo "line num: $nline"
    `sed -i '$d' $file_name`
    `sed -i '$d' $file_name`
    `sed -i '$d' $file_name`
    `sed -i '$d' $file_name`
    `sed -i '$d' $file_name`
    cat $file_name | awk '{print $3,$4}' > tmp
    cp tmp $file_name -f
    new_nline=`wc -l $file_name | awk '{ print $1 }'`
    echo "new line num: $new_nline"
done
