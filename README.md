# AccountantPlus Web Server [![Build Status](https://travis-ci.org/NjengaSaruni/Accountant-Web-Server.svg?branch=develop)](https://travis-ci.org/NjengaSaruni/Accountant-Web-Server) [![Coverage Status](https://coveralls.io/repos/github/NjengaSaruni/Accountant-Web-Server/badge.svg?branch=develop)](https://coveralls.io/github/NjengaSaruni/Accountant-Web-Server?branch=develop)
This repository contains the backend for the AccountantPlus web service. 

## How to run the server
1. ### Without Docker
    
   Install docker and docker-compose
   
   Spin up a server instance
   
   ```
   $ docker-compose up --build
   ``` 
2. ### Without docker (Linux | Ubuntu)

     
     $ git clone https://github.com/NjengaSaruni/Accountant-Web-Server.git
    
     $ cd Accountant-Web-Server    
    
 If you do not have python and pip installed:
 
     $ sudo apt-get install python3 python3-pip virtualenvwrapper
     
 Use of a virtual environment is recommended and is good practice
     
     $ mkvirtualenv -p /usr/bin/python3 <venv_name>
     $ workon <venv_name>
 
 Install packages from the requirements folder.
     
     $ pip install -r requirements/base.txt
     
 This Web API uses a PostgreSQL database. You need a PostgreSQL server running locally.
     
     $ sudo apt-get install postgresql postgresql-contrib
     
 Add a database to your Postgres server instance. You may use `psql` as follows:
 
         $ sudo -su postgres psql postgres
     
         # This will open an interactive terminal, where you can create a database, and a role. For tests, give your use the create db privilege
        
         > CREATE DATABASE <your_db_name>;
         > CREATE ROLE <your_user> LOGIN PASSWORD '<your_password>';
         > GRANT ALL PRIVILEGES ON DATABASE <your_db_name> TO <your_user>;
         > ALTER USER <your_user> CREATEDB;
         > \q
     

 Copy the values of the `.sample_env` file in the root folder into a new `.env` file
      
     $ cat .sample_env >> .env
     
 You can then use the `./manage.py` script to run migrations and run the dev server
 
     $ ./manage.py migrate
     $ ./manage.py createsuperuser
     $ ./manage.py runserver
     
 Maintained by [Peter Njenga](https://twitter.com/NjengaSaruni)
