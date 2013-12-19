#!/bin/python

""" 
This script will put assignments into the checked out repo

Input : List of students ids, assignment-id, commit message

"""

import sys
import os
import json
from subprocess import call

import requests
from requests.auth import HTTPBasicAuth

BB_USERNAME = 'avinassh'
BB_PASSWORD = 'ohlongjohnson'
BB_REPO_BASE_URL = 'https://%s:%s@bitbucket.org/%s/' % (BB_USERNAME, BB_PASSWORD, BB_USERNAME)
#BB_REPO_BASE_URL =  "git@bitbucket.org:%s/" % BB_USERNAME

students_info = json.loads(open('students-info.json', 'r').read())

assignment_path = '../../master-repo/assignments/assignment-1'

def main():
    os.chdir('students-repo-directory')
    for student_id, student_email in students_info.iteritems():
        os.chdir(student_id)
        student_repo_url = "%s%s.git" % (BB_REPO_BASE_URL, student_id)
        call('git pull', shell=True)
        call("git commit -m 'commit before adding assignment'", shell=True)
        rsync =  'rsync -r %s assignments/' % assignment_path
        #print rsync
        call(rsync, shell=True)
        call('git add .', shell=True)
        call("git commit -m 'commit after adding assignments'", shell=True)
        call("git push", shell=True)
        os.chdir('..')
        

if __name__ == '__main__':
            main()       
            #print BB_REPO_BASE_URL 