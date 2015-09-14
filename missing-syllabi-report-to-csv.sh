#!/usr/bin/env bash
# usage:
# missing-syllabi-report-to-csv.sh equella-report.txt > missing.csv
REPORT="$1"
sed -e 's/  :  /","/g' $REPORT > tmp
cat tmp | while read line; do
    echo "\"$line\""
done;
rm tmp
