# MoodService

**MoodService is a example project completed as part of a coding challenge, it is a good representation of my Python and Flask skills.**

## Prerequisites
```
Flask
APScheduler
bcrypt
```

## Running the tests
This project uses tox as a test runner, run the following commands from the root of the repo:
```
pip install tox
tox
```

## Running the app locally
Install via setup.py and then run as you would any other flask app. Requires Python 3.7:
```
pip install .
python MoodService/app.py
```

## Running the app via docker
```
docker pull willcipriano/mood_service
docker run -d -p 5000:5000 mood_service
```

## API
```
/register (POST)
- requires form parameters 'username' and 'password'
Allows a user to create an account

/login (POST)
- requires form parameters 'username' and 'password'
Allows a user to login, returns a session token to be used later

/mood (POST)
- requires form parameters 'token' and 'mood'
Allows the user to set their daily mood, returns the percentile they are in if it's over 50%

/mood (GET)
- requires form parameter 'token'
Allows the user to get all previous moods they have set

/mood (PATCH)
- requires form parameters 'token' and 'mood'
Allows the user to update their current mood
```

## Insomnia

A Insomnia configuration file is provided in /etc


## Issues
As this is a toy example, a few corners were cut for the sake of time. I have created a number of issue tickets that describe what would be required to bring this toy example into a production environment.

## Commits

As this was completed for a assessment I made some major commits every epoch or so, but also left all the branches dangling if a higher resolution view is required.
