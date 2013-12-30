#!/bin/python

""" 
This script will take assignment solutions from each student repository. Based 
on the timestamp given, it finds out the last commit made before timestamp 
(i.e. deadline) and it checks out that revision, rsyncs the solution folder 
of the required assignment with the solutions-repo.

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

from dir_settings import *

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


def sync_solutions():
    assignment_id = 'assignment-1'
    call('git pull', shell=True)
    commit_hash = get_commit_hash('Dec 20 22:31:01 2013')
    call('git checkout %s' % commit_hash, shell=True)
    source_path = 'assignments/%s/solutions' % assignment_id
    dest_path = '%s%s/%s/' % (SOLUTIONS_REPO, student_id, assignment_id)
    call('rsync  %s %s' % (source_path, dest_path))


def main():
    for student_id, student_email in students_info.iteritems():
        os.chdir(STUDENTS_REPO_DIRECTORY)
        os.chdir(student_id)
        sync_solutions()

if __name__ == '__main__':
    main()
