Deploy Docker-compose
-----------------
Step 1: Clone repository
~~~~
$ git clone https://github.com/nelsonguillerm7/hits
~~~~
Step 2: Deploy Docker Compose

Deploy on your server using `docker-compose -f <file> up -d`:

~~~~
$ docker-compose up -d --build
~~~~

Step 3: Execute migrations e import data

~~~~
$ docker exec -it hits bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py loaddata authentication.json
~~~~