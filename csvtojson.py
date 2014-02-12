""" This script will convert the CSV (downloaded from Google docs) to JSON
in following format 

{
    "201301007" : "a@vlabs.ac.in",
    "201301002" : "someguy@vlabs.ac.in",
    "201301003" : "anotherguy@gmail.com"
}

and it will save it as students-info.json

usage:
$python csvtojson.py mycsv.csv
"""

import sys
import csv
import json


def csvtojson():
    data = {}
    for row_no, student_id, student_name, student_email in csv.reader(open(sys.argv[1])):
        data[student_id] = student_email
    f = open('students-info.json', 'w+') 
    f.write(json.dumps(data))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage:\ncsvtojson <filepath>\n')
        sys.exit()
    csvtojson()