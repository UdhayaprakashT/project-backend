Split_bills
=======================

### Project Setup
1. Fork this repository (git@github.com:hashedin/splitpay.git). 
2. Clone the forked repository.
3. Go to folder split_bills. (i.e. - cd split_bills) 
4. Create a virtual environment. (i.e. - virtualenv -p python3 venv)
5. Activate the environment. (i.e. - source venv/bin/activate)
6. Install the dependencies inside the environment. (i.e. - pip install -r requirements.txt)

### Database Setup
1. Login to your postgres. (i.e. psql)
2. Create a database split_pay. (i.e - create database split_pay;)
3. Make sure root user has access to this database.
4. Quit the postgres. (i.e. \q)
5. Run python3 manage.py migrate
6. Create admin user (python3 manage.py createsuperuser)


### Running Server
1. Run the server. (i.e - python3 manage.py runserver)

### Steps to migrate from models to the Database
1. Make migration files. (i.e. python3 manage.py makemigrations)
2. Apply the migrations on the database (i.e. python3 manage.py migrate)


