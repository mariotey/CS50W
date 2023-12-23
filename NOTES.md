## How to Create Local Repository and push to Github ##
1. git init @ repository
2. git add .
3. git commit -m "Initial Commit"
4. git remote add origin <repository_url>
5. git push origin master
6. git push --set-upstream origin master

## How to Clone Repository ##
1. git init @ repository
2. navigate to Profile -> Settings -> Developer settings -> Generate New Token
3. git clone https://<personal_access_token>@github.com/<github_account_username>/<github_repository>.git

## Create & Run Django Project ##
1. python -m django startproject "ProjectName"
2. cd "ProjectName"
3. python manage.py runserver

## Create App within Django Project
1. navigate to Django Project repository
2. python manage.py startapp "AppName"

## Create SQL database and query
1. navigate to repository
2. touch flights.sql
3. sqlite3 flights.sql
4. sqlite> CREATE TABLE flights(
   ...>     id INTEGER PRIMARY KEY AUTOINCREMENT,
   ...>     origin TEXT NOT NULL,
   ...>     destination TEXT NOT NULL,
   ...>     duration INTEGER NOT NULL
   ...> );

## Create and implement migrations
1. navigate to Django Project repository
2. python manage.py makemigrations
3. python manage.py migrate

## How to manipulate SQL database in Linux terminal
1. navigate to Django Project repository
2. python manage.py shell
3. >>> from auctions.models import *
4. >>> Listing.objects.all()
5. >>> "SQL Query Commands"

## Create superuser account in web app for admin
1. navigate to Django Project repository
2. python manage.py createsuperuser
3. Username (leave blank to use 'workspace'): mariotey
4. Password:
5. Password (again):
6. Superuser created successfully
