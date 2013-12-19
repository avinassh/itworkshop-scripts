#!/bin/python

""" 
This script will delete all the repos of students on the Bitbucket

Input : List of students ids, Bitbucket credentials

"""

import sys
import json

import requests
from requests.auth import HTTPBasicAuth

BB_USERNAME = 'avinassh'
BB_PASSWORD = 'ohlongjohnson'
REPO_API_URL = 'https://api.bitbucket.org/2.0/repositories'

students_info = json.loads(open('students-info.json', 'r').read())

def delete_repo(repo_name):
    auth = HTTPBasicAuth(BB_USERNAME, BB_PASSWORD)
    url = '%s/%s/%s' % (REPO_API_URL, BB_USERNAME, repo_name)
    response = requests.delete(url=url, auth=auth)
    print response.status_code

def main():
    for student_id, student_email in students_info.iteritems():
        delete_repo(student_id)
        

if __name__ == '__main__':
            main()        