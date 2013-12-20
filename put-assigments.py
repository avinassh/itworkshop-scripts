#!/bin/python

""" 
This script will put assignments into the student repositories. First add new
assignments in master-repo/assignments and commit your changes. The directory 
name of the newly added assignment is the assignment id (assignment-x) is required. 
The script will first pull the student's repo from bitbucket, commit it and 
then rsync the newly added assignment directory to the repo and then push it.

Input : List of students ids, assignment-id, commit message

"""

# todo : what if the student update the repo during this process

import sys
import os
import json
from subprocess import call

import requests
from requests.auth import HTTPBasicAuth

from dir_settings import *

BB_USERNAME = 'avinassh'
BB_PASSWORD = 'ohlongjohnson'
BB_REPO_BASE_URL = 'https://%s:%s@bitbucket.org/%s/' % (BB_USERNAME, BB_PASSWORD, BB_USERNAME)
#BB_REPO_BASE_URL =  "git@bitbucket.org:%s/" % BB_USERNAME

students_info = json.loads(open('students-info.json', 'r').read())

assignment_path = '../../master-repo/assignments/assignment-1'

def main():
    os.chdir(STUDENTS_REPO_DIRECTORY)
    for student_id, student_email in students_info.iteritems():
        os.chdir(student_id)
        student_repo_url = "%s%s.git" % (BB_REPO_BASE_URL, student_id)
        call('git pull', shell=True)
        call("git commit -m 'commit before adding assignment'", shell=True)
        rsync =  'rsync -r %s assignments/' % assignment_path
        call(rsync, shell=True)
        call('git add .', shell=True)
        call("git commit -m 'commit after adding assignments'", shell=True)
        call("git push", shell=True)
        os.chdir(STUDENTS_REPO_DIRECTORY)
        

if __name__ == '__main__':
            main()