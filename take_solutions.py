#!/bin/python

""" 
This script will take assignment solutions from each student repository. Based 
on the timestamp given, it finds out the last commit made before timestamp 
(i.e. deadline) and it checks out that revision, rsyncs the solution folder 
of the required assignment with the solutions-repo and resets to HEAD.

The timestamp should be of the format 'Month Date H:M:S Year' 

eg. Dec 19 22:31:01 2013

Input : List of students ids, assignment-id, timestamp

Example usage: To take out solutions of assignment 11 whose deadline was 
Dec 19 22:31:01 2013, run the following

$python take_solutions.py -d 'Dec 19 22:31:01 2013' -aid 'assignment-11'


To do: 
- git_log_cmd with format string in get_commit_hash()
- dest_path should be global?
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
import argparse
import shlex

from dir_settings import *
from bb_settings import *

SOLUTIONS_DIRECTORY = 'solutions-directory/'
STUDENTS_REPO_DIRECTORY = 'students-repo-directory/'

parser = argparse.ArgumentParser(description='This script will take assignment solutions from each student repository. Based on the timestamp given, it finds out the last commit made before timestamp (i.e. deadline) and it checks out that revision, rsyncs the solution folder of the required assignment with the solutions-repo and resets to HEAD.')
parser.add_argument('-d','--deadline', help='The timestamp should be of the \
                    format "Month Date H:M:S Year" e.g. "Dec 19 22:31:01 2013"', 
                    required=True)
parser.add_argument('-aid','--assignment_id', help='Please provide assignment \
                    id of the solutions you want to copy. e.g. assignment-7', 
                    required=True)
args = vars(parser.parse_args())

students_info = json.loads(open(STUDENTS_INFO, 'r').read())
assignment_id = args['assignment_id']
deadline = args['deadline']
DEST_PATH = SOLUTIONS_DIRECTORY + assignment_id + '-' + '-'.join(deadline.split()) + '/'


def get_commit_hash(repo_name, timestamp):
    git_log_cmd = shlex.split('git --git-dir=' + STUDENTS_REPO_DIRECTORY + repo_name + '/.git log --pretty=format:"%H %ad" --date=local')
    try:
        (output, error) = subprocess.Popen(git_log_cmd, stdout=subprocess.PIPE).communicate()
        for git_log in string.split(output, os.linesep):
            deadline = datetime.datetime.strptime(timestamp, "%b %d %H:%M:%S %Y")
            # split the commit message by first white space, the returning list will 
            # have hash as its first element and timestamp as second element
            commit_hash = git_log.split(' ', 1)[0] 
            commit_timestamp = git_log.split(' ', 1)[1]
            if deadline > datetime.datetime.strptime(commit_timestamp, "%a %b %d %H:%M:%S %Y"):
                return commit_hash
    except Exception, e:
        raise e


def sync_solutions(repo_name):
    def repo_exists(repo_name):
        return os.path.isdir(STUDENTS_REPO_DIRECTORY + repo_name)

    def clone_repo(repo_name):
        clone_cmd = shlex.split("git clone %s%s %s%s" % (BB_REPO_BASE_URL, 
                                repo_name, STUDENTS_REPO_DIRECTORY, repo_name))
        #print clone_cmd
        try:
            subprocess.check_call(clone_cmd)#, stdout=LOG_FD, stderr=LOG_FD)
        except Exception, e:
            raise e

    def pull_repo(repo_name):
        pull_cmd = shlex.split("git --git-dir=%s/.git pull" % \
                            (STUDENTS_REPO_DIRECTORY + repo_name))
        #print pull_cmd
        try:
            subprocess.check_call(pull_cmd)#, stdout=LOG_FD, stderr=LOG_FD)
        except Exception, e:
            raise e

    def checkout_version(repo_name, commit_hash='-'):
        try:
            checkout_cmd = shlex.split("git --git-dir=%s/.git checkout %s" \
                                % ((STUDENTS_REPO_DIRECTORY + repo_name), commit_hash))
            # print "git --git-dir=%s/.git checkout %s" \
            #                     % ((STUDENTS_REPO_DIRECTORY + repo_name), commit_hash)
            subprocess.check_call(checkout_cmd)#, stdout=LOG_FD, stderr=LOG_FD)
        except Exception, e:
            raise e


    def rsync(repo_name):
        src_path = STUDENTS_REPO_DIRECTORY + repo_name + '/assignments/' + assignment_id
        if not os.path.isdir(src_path):
            # either student messed up the dir structure or hasn't submitted his assginments
            return
        if not os.path.isdir(DEST_PATH + repo_name):
            os.makedirs(DEST_PATH + repo_name)
        rsync_cmd = 'rsync -rt %s %s' % (src_path, DEST_PATH + repo_name)
        subprocess.check_call(rsync_cmd, shell=True)

    if repo_exists(repo_name):
        pull_repo(repo_name)
    else:
        clone_repo(repo_name)

    commit_hash = get_commit_hash(repo_name, deadline)
    if commit_hash:
        checkout_version(repo_name, commit_hash)
        rsync(repo_name)
    else:
        #student has not made any commit before deadline
        return

    # call('git pull', shell=True)
    # commit_hash = get_commit_hash(deadline)
    # call('git checkout %s' % commit_hash, shell=True)
    # source_path = 'assignments/%s/solutions' % assignment_id
    # dest_path = '%s%s/%s/' % (SOLUTIONS_REPO, student_id, assignment_id)
    # call('rsync  %s %s' % (source_path, dest_path))
    # call('git checkout -', shell=True)


def main():
    if not os.path.isdir(STUDENTS_REPO_DIRECTORY):
        os.makedirs(STUDENTS_REPO_DIRECTORY)
    if not os.path.isdir(SOLUTIONS_DIRECTORY):
        os.makedirs(SOLUTIONS_DIRECTORY)
    if not os.path.isdir(DEST_PATH):
        os.makedirs(DEST_PATH)

    for student_id, student_email in students_info.iteritems():
        #os.chdir(STUDENTS_REPO_DIRECTORY)
        #os.chdir(student_id)
        #print i, student_id
        sync_solutions(student_id)


if __name__ == '__main__':
    main()
