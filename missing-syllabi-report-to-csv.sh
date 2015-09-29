#!/usr/bin/env bash
# usage:
# missing-syllabi-report-to-csv.sh equella-report.txt > missing.csv

# separator used in BIRT report
SEP='  :  '
sed -e "s/${SEP}/\",\"/g" "$1" | while read line; do
    echo "\"$line\""
done;
