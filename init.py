#!/bin/python

""" This script will initialize the local system, sets up the directory 
structure, creates master-repo, solutions-repo and directory containing 
all the students repo. The students repo will be initialized by adding a 
welcome message and also setting up git upstream url

input : List of students ids, Bitbucket credentials

Structure:

master-repo:
|-assignments
    |-assignment-1
        |-exercises
        |-solutions
    |-assignment-2
        |-exercises
        |-solutions
    .
    .
    .
    |-assignment-x
        |-exercises
        |-solutions        
|-other-data
|-README.md

solutions-repo:
|-201301001 (the student id)
    |-assignment-1
    |-assignment-2
    .
    .
    .
    |-assignment-x
|-201301002
.
.
|-20130X00X

directory containing all students repos:
student-repositories:
|-201301001 (the student id)
|-201301002
.
. 
.
|-20130X00X

student repo on Bitbucket:
|-201301001 (the student id is the repo name)
    |-assignments
        |-assignment-1
            |-exercises
            |-solutions
        |-assignment-2
            |-exercises
            |-solutions
        .
        .
        .
        |-assignment-x
            |-exercises
            |-solutions

"""

import os
from os import makedirs
import sys
import shutil
import json
from subprocess import call

from bb_settings import *
from dir_settings import *

students_info = json.loads(open(STUDENTS_INFO, 'r').read())

def init_solutions_repo():
    for student_id, student_email in students_info.iteritems():
        makedirs('solutions-repo/%s' % student_id)

def init_students_repo_directory():
    makedirs('students-repo-directory')
    for student_id, student_email in students_info.iteritems():
        makedirs('students-repo-directory/%s' % student_id)
        shutil.copy('master-repo/README.md', 'students-repo-directory/%s' % student_id)
        os.chdir('students-repo-directory/%s' % student_id)
        call('git init', shell=True)
        call('git add .', shell=True)
        call("git commit -m 'Initial commit'", shell=True)
        call('git remote add origin https://%s:%s@bitbucket.org/%s/%s.git' % (BB_USERNAME, BB_PASSWORD, BB_USERNAME, student_id), shell=True)
        call('git push -u origin master', shell=True)
        os.chdir('../../')

def init_master_repo():
    makedirs('master-repo/assignments/assignment-1')
    makedirs('master-repo/other-data')
    open(r'master-repo/README.md', 'w')
    open(r'master-repo/assignments/assignment-1/README.md', 'w')

init_master_repo()
init_solutions_repo()
init_students_repo_directory()