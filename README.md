# Plytix Challenge
Personal project for Plytix technical test.

## Download
You just need to clone this repo

 <code>
git clone https://github.com/pabloantondp/PlytixChallenge.git
 </code>

## Build and running
Project can be build using docker-component tool. First you need is to install docker in your system
https://docs.docker.com/get-docker/

Go to project folder and execute docker-compose:

<code>
    
    cd PlytixChallenge

    docker-compose build

    docker-compose up -d

That will create two services:

- Mongodb service listening on port 27017
- Flask server listening on port 8080

From this point on, API endpoints are accessible in:
http://localhost:8080/words

## Documentation
Project uses flask_restx to generate REST API documentation. You just need to access to:

http://localhost:8080/

## Running test
Project uses pytest framework to run unit test. You can launch them inside the docker container:

<code>
docker-compose exec flask pytest "flaskr/test"

## Troubleshooting

Docker files are prepared to run into a linux distribution without any change. Nevertheless,
if you plan to run it in a windows host, you will need to remove next configuration from the
docker-compose.yml file:

<code>
    network_mode: host

MacOSX host has not been tested at all.