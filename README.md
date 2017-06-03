# Dota 5 Stack

## About
Personally, I hate playing with pub randoms. Yes, you will find a fun person to play with occasionally - but the anonymity usually brings out the worst in people. I want to help build the community. In my case, the Australian community of all skill levels. 


## Set up

Set up (optional)

```py
# install a virtual environment
pip install virtualenv

# make a virtual environment
mkvirtualenv dota5stack
```

Installation 

```py
# install python requirements
pip install -r requirement.txt

# set up database
dropdb dota-db
createdb dota-db
python manage.py db upgrade

# start server
python app.py

# Runs in port 3000
# http://localhost:3000/
```

## Technologies used:
Languages:

- Python
- SQL
- Postgress

Libraries:

- Flask
- Steam API
- bcrypt

## To do:


- Implimiment buttons to use AJAX and jQuery
- Plan and style information of offline and online lists
- Profile page to include a small bio of the user
- Pending and accepting team invites (currently captain invites people to teams) 
	- Status:
		- 1 - Pending
		- 2 - Joined
		- 3 - Captain
