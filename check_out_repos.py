#!/bin/python

""" 
This script will check out all the student git repos and they will be kept in
students-repo-directory  

Input : List of students ids, Bitbucket credentials

"""

import sys
import os
import json
from subprocess import call

import requests
from requests.auth import HTTPBasicAuth

MASTER_REPO = '/Users/avi/Desktop/itworkshop/master-repo/'
STUDENTS_REPO_DIRECTORY = '/Users/avi/Desktop/itworkshop/students-repo-directory/'
SOLUTIONS_REPO = '/Users/avi/Desktop/itworkshop/solutions-repo/'

BB_USERNAME = 'avinassh'
BB_PASSWORD = 'ohlongjohnson'
BB_REPO_BASE_URL = "https://%s:%s@bitbucket.org/%s/" % (BB_USERNAME, BB_PASSWORD, BB_USERNAME)
#BB_REPO_BASE_URL =  "git@bitbucket.org:%s/" % BB_USERNAME

students_info = json.loads(open('students-info.json', 'r').read())

def main():
    os.chdir(STUDENTS_REPO_DIRECTORY)
    for student_id, student_email in students_info.iteritems():
        git_clone = 'git clone %s%s.git' % (BB_REPO_BASE_URL, student_id)
        call(git_clone, shell=True)
        
if __name__ == '__main__':
            main()