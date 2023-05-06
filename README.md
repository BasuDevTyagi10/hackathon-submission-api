# hackathon-submission-api

## Instructions for running the application

### Getting Started

Clone the repository and move to the root directory
```commandline
$ git clone https://github.com/BasuDevTyagi10/hackathon-submission-api.git
$ cd hackathon-submission-api
```

### Running the API
There are two ways to run this application, one is via Docker and the other is simply through python (with requires all the dependencies to be managed manually) 

#### Running with Docker

Make sure you are in the root directory having the `docker-compose.yml` and `Dockerfile`.

Run the following commands to build the images and start the containers:

```commandline
$ docker compose -d
```

As defined in the `docker-compose.yml` file, it will pull the postgres image and create the required database with the required credentials. It will also create the api image using the Dockerfile and also the network over which these two containers will share data. The compose file will also run the migrations and then start the server.

The API is now up and running and will be serving requests at http://localhost:8000/api

**To Access the Admin Dashboard:**

The Django admin dashboard is only accessible to registered users. In order to create a superuser to access the dashboard, run the following commands:

```commandline
$ docker exec -it <container-name/id-of-api> bash
```

This will open the shell for the api application. The container name/id can be found using the command below:

```commandline
$ docker ps
```

```text
    OUTPUT:
    CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                    NAMES
    7496efa1bd2a   ai-planet-assignment-api   "sh -c 'python hacka…"   39 seconds ago   Up 37 seconds   0.0.0.0:8000->8000/tcp   ai-planet-assignment-api-1
    1907ca1fb1fa   postgres                   "docker-entrypoint.s…"   40 seconds ago   Up 38 seconds   5432/tcp                 ai-planet-assignment-db-1
```

Once the shell is open, run the commands below to create the user:

```commandline
# python hackathon_submission/manage.py createsuperuser
```

The command will prompt you to provide the credentials like username, email and password. Once done, close the shell using:

```commandline
# exit
```

Head over to http://localhost:8000/admin to access the Django Dashboard.

#### Running with Python

Running by this method requires the dependencies like Python and Postgres to be managed manually. This project is built using Python 3.10 and PostgreSQL 14.7, which must be installed and set up separately.

Log into Postgres using the shell command `psql` and providing the password used during installation. Run the following SQL expressions to create the database and the user to access the database.

```sql
    CREATE DATABASE hackathon_submission;
    
    CREATE USER aiplanet WITH ENCRYPTED PASSWORD 'admin';
     
    ALTER ROLE aiplanet SET client_encoding TO 'utf8';
    ALTER ROLE aiplanet SET default_transaction_isolation TO 'read committed';
    ALTER ROLE aiplanet SET timezone TO 'UTC';
    
    GRANT ALL PRIVILEGES ON DATABASE hackathon_submission TO aiplanet;
```

Exit the psql shell using `\q`.

After the database setup. Run the following commands to start the application using the instructions below:

1. Install virtualenv in Python using the commands below:
    ```commandline
    $ pip install virtualenv
    $ virtualenv venv
    ```
2. Next create a virtual environment to install all python dependencies and activate it:
    ```commandline
    $ virtualenv venv
    ```
   On Linux/MacOS:
    ```commandline
    $ source venv/Scripts/activate
    ```
   On Windows:
    ```commandline
    $ cd venv/Scripts/
    $ activate.bat
    ```
3. Install the required dependencies:
    ```commandline
    $ pip install -r requirements.txt
    ```
4. Create a `.env` file using the `env.template` file. Run the below command:
    ```commandline
    $ cp env.template .env
    ```
5. Run the migrations and start the server using:
    ```commandline
    $ python hackathon_submission/manage.py migrate
    $ python hackathon_submission/manage.py runserver 0.0.0.0:8000
    ```
   
Again, to access the Admin Dashboard you will have to create a superuser as follows:
```commandline
$ python hackathon_submission/manage.py createsuperuser
```

The command will prompt you to provide the credentials like username, email and password.

### Available Endpoints:

The details of the available endpoints are provided here:
https://documenter.getpostman.com/view/25447879/2s93eX2DXH
