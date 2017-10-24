# Computational Thinking Engine

The vision:
A tool that allows teachers to access, customise and interact with the curriculum. A place that students can log on to take assessment and feedback surveys, as well as perhaps do some interactive problems and games. 

--------------------------------------------------

Getting started:
1) download python (v.3.6.3)
 - make sure python is added to your path
2)open command prompt and run:
 - pip install Flask
 - pip install Flask-PyMongo
 - pip install bcrypt

To run the project:
1) Open command prompt
2) Go to directory with python script eg. cd Documents...
3) run -> python filename.py
4) Open browser and enter 127.0.0.1:5000 

Or:
1) Using the Sublime Text 3 text editor
2) open python script and click ctrl-b
3) Open browser and enter 127.0.0.1:5000 

------------------------------------------------------------

Using mLab - mLab is the largest cloud MongoDB service in the world.

In mLab I have a users collection: 
Student:
user_type,
school,
name,
surname,
approved,
user_id,
password

Instructor:
user_type,
school,
title,
name,
surname,
email,
password

What i have so far:
Home page:
Register for both instructor & student
Sign in
Profile

Issues: Students cant sign in yet.
