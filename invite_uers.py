#!/bin/python

""" 
This script will send the invitation email to the all the students 

Input : List of students (their ids and email ids), Bitbucket credentials

"""

import sys
import json

import requests
from requests.auth import HTTPBasicAuth

BB_USERNAME = 'avinassh'
BB_PASSWORD = 'ohlongjohnson'
INVITE_API_URL = 'https://bitbucket.org/api/1.0/invitations/'

students_info = json.loads(open('students-info.json', 'r').read())

def invite_user_to_repo(repo_name, invitee_email):
    auth = HTTPBasicAuth(BB_USERNAME, BB_PASSWORD)
    # the request URL format is https://bitbucket.org/api/1.0/invitations/BB_USERNAME/repo_name/invitee_email
    url = '%s/%s/%s/%s' %(INVITE_API_URL, BB_USERNAME, repo_name, invitee_email)
    payload = { "permission" : "write" } 
    response = requests.post(url=url, data=payload, auth=auth)
    print repo_name, response.status_code
    #print response.text

def main():
    for student_id, student_email in students_info.iteritems():
        invite_user_to_repo(student_id, student_email)

if __name__ == '__main__':
            main()        