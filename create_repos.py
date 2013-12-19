#!/bin/python

""" 
This script will create private repos on Bitbucket and send the invitation 
email to the all the student 

Input : List of students (name and their email ids), Bitbucket credentials

"""

import sys
import json

import requests
from requests.auth import HTTPBasicAuth

BB_USERNAME = 'avinassh'
BB_PASSWORD = 'ohlongjohnson'
REPO_API_URL = 'https://api.bitbucket.org/2.0/repositories/'
INVITE_API_URL = 'https://bitbucket.org/api/1.0/invitations/'

students_info = json.loads(open('students-info.json', 'r').read())

def create_repo(repo_name):
    auth = HTTPBasicAuth(BB_USERNAME, BB_PASSWORD)
    url = REPO_API_URL+BB_USERNAME+'/'+repo_name
    payload = { "scm": "git", "is_private": "true"}
    headers = {'content-type': 'application/json'}
    response = requests.post(url=url, data=payload, auth=auth)
    print repo_name, response.status_code
    #print response.text

def invite_user_to_repo(repo_name, invitee_email):
    auth = HTTPBasicAuth(BB_USERNAME, BB_PASSWORD)
    url = INVITE_API_URL+BB_USERNAME+'/'+repo_name+'/'+invitee_email
    payload = { "permission" : "write" } 
    response = requests.post(url=url, data=payload, auth=auth)
    print repo_name, response.status_code
    #print response.text

def main():
    for student_id, student_email in students_info.iteritems():
        create_repo(student_id)
        #invite_user_to_repo(student_id, student_email)

if __name__ == '__main__':
            main()        