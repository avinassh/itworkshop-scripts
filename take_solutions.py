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
- dest_path is ugly
- dest_path should be global?  
- Ruler: 78!!
"""


import string
import os
import time
import datetime
import subprocess
import json
import argparse
import shlex
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler

from dir_settings import *
from bb_settings import *

parser = argparse.ArgumentParser(description='This script will take assignment solutions from each student repository. Based on the timestamp given, it finds out the last commit made before timestamp (i.e. deadline) and it checks out that revision, rsyncs the solution folder of the required assignment with the solutions-repo and resets to HEAD.')
parser.add_argument('-d','--deadline', help='The timestamp should be of the \
                    format "Month Date H:M:S Year" e.g. "Dec 19 22:31:01 2013"', 
                    required=True)
parser.add_argument('-aid','--assignment_id', help='Please provide assignment \
                    id of the solutions you want to copy. e.g. assignment-7', 
                    required=True)

NITRO_LOGGER = logging.getLogger('NITRO')
LOG_FILENAME = 'nitro.log'
SOLUTIONS_DIRECTORY = 'solutions-directory/'
STUDENTS_REPO_DIRECTORY = 'students-repo-directory/'
students_info = json.loads(open(STUDENTS_INFO, 'r').read())
DEST_PATH = SOLUTIONS_DIRECTORY + assignment_id + '-' + '-'.join(deadline.split()) + '/'

args = vars(parser.parse_args())
assignment_id = args['assignment_id']
deadline = args['deadline']


def get_commit_hash(repo_name, timestamp):
    git_log_cmd = shlex.split('git --git-dir=' + STUDENTS_REPO_DIRECTORY + repo_name + '/.git log --pretty=format:"%H %ad" --date=local')
    try:
        (output, error) = subprocess.Popen(git_log_cmd, stdout=subprocess.PIPE, stderr=LOG_FD).communicate()
        for git_log in string.split(output, os.linesep):
            deadline = datetime.datetime.strptime(timestamp, "%b %d %H:%M:%S %Y")
            # split the commit message by first white space, the returning list will 
            # have hash as its first element and timestamp as second element
            commit_hash = git_log.split(' ', 1)[0] 
            commit_timestamp = git_log.split(' ', 1)[1]
            if deadline > datetime.datetime.strptime(commit_timestamp, "%a %b %d %H:%M:%S %Y"):
                return commit_hash
    except Exception, e:
        NITRO_LOGGER.error("git clone failed for repo %s: %s" % (repo_name, str(e)))
        #raise e
        

def sync_solutions(repo_name):

    def repo_exists(repo_name):
        return os.path.isdir(STUDENTS_REPO_DIRECTORY + repo_name)

    def clone_repo(repo_name):
        clone_cmd = shlex.split("git clone %s%s %s%s" % (BB_REPO_BASE_URL, 
                                repo_name, STUDENTS_REPO_DIRECTORY, repo_name))
        # NITRO_LOGGER.debug(clone_cmd)
        try:
            subprocess.check_call(clone_cmd, stdout=LOG_FD, stderr=LOG_FD)
        except Exception, e:
            NITRO_LOGGER.error("git clone failed for repo %s: %s" % (repo_name, str(e)))

    def pull_repo(repo_name):
        pull_cmd = shlex.split("git --git-dir=%s/.git pull" % \
                            (STUDENTS_REPO_DIRECTORY + repo_name))
        # NITRO_LOGGER.debug(pull_cmd)
        try:
            subprocess.check_call(pull_cmd, stdout=LOG_FD, stderr=LOG_FD)
        except Exception, e:
            NITRO_LOGGER.error("git pull failed for repo %s: %s" % (repo_name, str(e)))

    def checkout_version(repo_name, commit_hash='-'):
        try:
            checkout_cmd = shlex.split("git --git-dir=%s/.git checkout %s" \
                                % ((STUDENTS_REPO_DIRECTORY + repo_name), commit_hash))
            # NITRO_LOGGER.debug(checkout_cmd)
            # I want to ignore the entire output of checkout_cmd
            subprocess.check_call(checkout_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception, e:
            NITRO_LOGGER.error("git checkout failed for repo %s tag %s: %s" % (repo_name, commit_hash, str(e)))
            #raise e


    def rsync(repo_name):
        src_path = STUDENTS_REPO_DIRECTORY + repo_name + '/assignments/' + assignment_id
        if not os.path.isdir(src_path):
            # either student messed up the dir structure or hasn't submitted his assignments
            return
        if not os.path.isdir(DEST_PATH + repo_name):
            os.makedirs(DEST_PATH + repo_name)
        rsync_cmd = shlex.split('rsync -rt %s %s' % (src_path, DEST_PATH + repo_name))
        subprocess.check_call(rsync_cmd, stdout=LOG_FD, stderr=LOG_FD)

    if repo_exists(repo_name):
        pull_repo(repo_name)
    else:
        clone_repo(repo_name)

    commit_hash = get_commit_hash(repo_name, deadline)
    if commit_hash:
        checkout_version(repo_name, commit_hash)
        rsync(repo_name)
        checkout_version(repo_name)
    else:
        #student has not made any commit before deadline
        return


def setup_logging():
    NITRO_LOGGER.setLevel(logging.DEBUG)   # make log level a setting
    # Add the log message handler to the logger
    myhandler = TimedRotatingFileHandler(LOG_FILENAME, when='midnight', 
                                        backupCount=5)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S %p')
    myhandler.setFormatter(formatter)
    NITRO_LOGGER.addHandler(myhandler)
    

def init():
    if not os.path.isdir(STUDENTS_REPO_DIRECTORY):
        os.makedirs(STUDENTS_REPO_DIRECTORY)
    if not os.path.isdir(SOLUTIONS_DIRECTORY):
        os.makedirs(SOLUTIONS_DIRECTORY)
    if not os.path.isdir(DEST_PATH):
        os.makedirs(DEST_PATH)


def main():
    NITRO_LOGGER.debug('****Firing up NITRO***')
    init()
    for student_id, student_email in students_info.iteritems():
        NITRO_LOGGER.debug(student_id)
        sync_solutions(student_id)
    NITRO_LOGGER.debug('****Done with NITRO***')


if __name__ == '__main__':
    LOG_FD = open(LOG_FILENAME, 'a')
    setup_logging()
    main()
