#Hello!

This repository contains the scripts required for the class IT Workshop Spring 2014 (ICS 105). The scripts here will create all the directories required on local machine, repositories for each student on Bitbucket and also provide provision for taking out assignment solutions from each student repository.

Following are the scripts should be run first (and only once).

- create_repos.py : This script will create repositories for each student on Bitbucket
- invite_users.py : This script will assign each student to their repository and also sends them an invite email
- init.py : This script will create the required directory structure on teacher's local machine. Run this only after create_repos.py as this script will also initialize the student repositories by setting proper upstream etc.

and then take_solutions.py script can be run whenever required. 

#Quick start:

- The students' email ID and university ID should be provided in JSON (see 'students-info.json') and the file path should be updated in dir_settings.py  
- Update the Bitbucket username and password in bb_settings file. Using these credentials students repositories will be created.
- Run create_repos.py and invite_users.py subsequently. 
- Run the init.py script to initialize the directory structure on the teacher's local machine. This script will work under current working directory and it will create directories : 'solutions-repo' and 'students-repo-directory'
- Update the dir_settings.py accordingly.
- ...
- Whenever assignment solutions need to be taken out from student repo, then run take_solutions.py. Example usage:
		
		$python take_solutions.py -d 'Dec 19 22:31:01 2013' -aid 'assignment-11'

#The directory structure:

master-repo (same as each student repository) :

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

Directory containing all students repos:

	student-repo-directory:
		|-201301001 (the student id)
		|-201301002
		.
		. 
		.
		|-20130X00X

Student repo on Bitbucket:

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
