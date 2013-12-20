#!/bin/python

""" 
This script will take assignment solutions from each student repository. First
it will clone the repository in a temporary location. Based on the
timestamp given, it finds out the last commit made before timestamp and it 
checks out that revision, rsyncs the solution folder of the required assignment 
with the solutions-repo.

The timestamp should be of the format 'Month Date H:M:S Year' 

eg. Dec 19 22:31:01 2013

Input : List of students ids, assignment-id, timestamp

"""


import string
import os
import time
import datetime
import subprocess
from subprocess import call
import shutil
import tempfile
import json

MASTER_REPO = '/Users/avi/Desktop/itworkshop/master-repo/'
STUDENTS_REPO_DIRECTORY = '/Users/avi/Desktop/itworkshop/students-repo-directory/'
SOLUTIONS_REPO = '/Users/avi/Desktop/itworkshop/solutions-repo/'
# build a dictionary of the commit log
# commit_logs = {} 

#given_timestamp = datetime.datetime.strptime('Dec 20 22:31:01 2013', "%b %d %H:%M:%S %Y")

students_info = json.loads(open('students-info.json', 'r').read())

def get_commit_hash(timestamp):
    (output, error) = subprocess.Popen('git log --pretty=format:"%H %ad" --date=local', 
        stdout=subprocess.PIPE, shell=True).communicate()
    for git_log in string.split(output, os.linesep):
        deadline = datetime.datetime.strptime(timestamp, "%b %d %H:%M:%S %Y")
        # split the commit message by first white space, the returning list will 
        # have hash as its first element and timestamp as second element
        commit_hash = git_log.split(' ', 1)[0] 
        commit_timestamp = git_log.split(' ', 1)[1]
        if deadline > datetime.datetime.strptime(commit_timestamp, "%a %b %d %H:%M:%S %Y"):
            return commit_hash

#commit_hash = get_commit_hash('Dec 20 22:31:01 2013')
#print commit_hash

def sync_solutions():
    try:
        assignment_id = 'assignment-1'
        student_repo_path = os.getcwd()
        call('git pull', shell=True)
        tmp_dir = tempfile.mkdtemp()
        call('rsync -r %s %s' %(student_repo_path, tmp_dir), shell=True)
        os.chdir(tmp_dir)
        commit_hash = get_commit_hash('Dec 20 22:31:01 2013')
        call('git checkout %s' % commit_hash, shell=True)
        source_path = 'assignments/%s/solutions' % assignment_id
        dest_path = '%s%s/%s/' % (SOLUTIONS_REPO, student_id, assignment_id)
        call('rsync  %s %s' % (source_path, dest_path))
    finally:
        try:
            shutil.rmtree(tmp_dir)
        except OSError as exc:
            if exc.errno != 2:
                raise

#steps, 
# change to 'students-repo-directory' and iterate over each repo
# do git pull to get the latest repo and make a copy of it in a temporary location
# get the commit hash and check out the folder to that hash
# sync the assignment-id solutions folder with the appropriate students solution directory in solutions repo

def main():
    os.chdir(STUDENTS_REPO_DIRECTORY)
    for student_id, student_email in students_info.iteritems():
        os.chdir(student_id)
        sync_solutions()
        #call('git pull', shell=True)
        os.chdir(STUDENTS_REPO_DIRECTORY)

if __name__ == '__main__':
    main()
