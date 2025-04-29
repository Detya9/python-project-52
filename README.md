# Task Manager
[![Actions Status](https://github.com/Detya9/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Detya9/python-project-52/actions)
[![Python CI](https://github.com/Detya9/python-project-52/actions/workflows/pyci.yml/badge.svg?branch=main)](https://github.com/Detya9/python-project-52/actions/workflows/pyci.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Detya9_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Detya9_python-project-52)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Detya9_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Detya9_python-project-52)
## App's Link
Click [here](https://python-project-52-zwm5.onrender.com)
### Used tools:
Python, Django, Django-Bootstrap, Django-filter, Bootstrap5, gunicorn
### Installation:
First of all you need to install uv:
```
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```
```
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Then copy project to your computer:
```
git clone git@github.com:Detya9/python-project-52.git
```
And run:
```
make install
```
### Start working:
Create the new .env file and define SECRET_KEY, DEBUG, DATABASE_URL and WEB_CONCURRENCY variables there.

For example:
```
SECRET_KEY='fake_secret_key'
DEBUG = True for development or False for production
DATABASE_URL = 'postgresql://user:password@host:port/database_name'
WEB_CONCURRENCY = 4
```
For development:
```
make start
```
For production:
```
make render-start
```
