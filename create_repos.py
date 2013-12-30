#!/bin/python

""" 
This script will create private repositories on Bitbucket for each student.
The repo name will be same as the university ID of the student.

Input : List of students ids, Bitbucket credentials

"""

import sys
import json

import requests
from requests.auth import HTTPBasicAuth

from bb_settings import *
from dir_settings import *

students_info = json.loads(open(STUDENTS_INFO, 'r').read())

def create_repo(repo_name):
    auth = HTTPBasicAuth(BB_USERNAME, BB_PASSWORD)
    # the request URL format is https://api.bitbucket.org/2.0/repositories/BB_USERNAME/repo_name
    url = '%s%s/%s' % (REPO_API_URL, BB_USERNAME, repo_name)
    payload = { "scm": "git", "is_private": "true"}
    headers = {'content-type': 'application/json'}
    response = requests.post(url=url, data=payload, auth=auth)
    print repo_name, response.status_code
    #print response.text

def main():
    for student_id, student_email in students_info.iteritems():
        create_repo(student_id)

if __name__ == '__main__':
            main()        