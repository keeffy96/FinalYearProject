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

Fixed:
Added a superUser, userTable shows all users
Finished bebras1 & bebras2
Added nice pie chart graph on UserTable click
Updated home
Updated UserTable -> clickable -> studentprogress
Updated student sign-up -> bebrasTest -> home added restriction if user is not approved


To be implemented:
Add class as discussed - talk about what will student do? or will teacher assign student to class?
Add simple student survey - when will student complete this? after sign up? or add section in My Profile to complete?
Add alternative answers for a few bebras1 questions
Add pictures to bebras2

------------------------------------------------------------
Researching best way to store comments in the database

correct andsers sudent progress


Issues: 
Need GridFS working on the server, it works locally.

