# Pivas BOT

## Project Structure
- frontend
- backend
	- backend - django-admin application
	- website - JSON-API for frontend
	- steambot - Bot Application

## How to start server
Web server is written on Python 3.7
Download: https://www.python.org/downloads/
Windows: Allow add to PATH

### Set enviroment variables

`STEAM_API_KEY=0151AD3CCB9F86DED7B1B7A9EF078A6F
PYTHONPATH=backend
DJANGO_SETTINGS_MODULE=backend.settings
DEBUG=True
`
#### Linux
`direnv allow`

#### Windows
https://helpdeskgeek.com/how-to/create-custom-environment-variables-in-windows/

Load packages: `$ pip3 install -r backend/requirements.txt`

## Run Django Server from project root
Linux: `django-admin runserver`
Windows: `python backend\manage.py runserver`

Now you can control DataBase via Django Admin: http://127.0.0.1:8000/admin/, acc and pass in slack

## Backend JSON API endpoints
http://127.0.0.1:8000/api/getExample/ - GET example
