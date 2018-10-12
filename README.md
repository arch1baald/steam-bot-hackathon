# Pivas BOT

## Project Structure
- frontend
- backend
	- backend -- django-admin application
	- website -- JSON-API for frontend
	- steambot -- Bot Application

## How to start server
Web server is written on Python 3.7 https://www.python.org/downloads/
Set enviroment variables: direnv allow https://github.com/direnv/direnv/issues/343
Load packages: pip3 install -r backend/requirements.txt
Run Django Server from project root: django-admin runserver

Now you can control DataBase via Django Admin: http://127.0.0.1:8000/admin/, acc and pass in slack

## Backend API endpoints
http://127.0.0.1:8000/api/getExample/ - JSON API response example
