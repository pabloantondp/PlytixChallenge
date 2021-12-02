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

Go to project folder an execute docker-compose:

<code>
    cd PlytixChallenge<br/>
    docker-compose build<br/>
    docker-compose up -d
</code>

That will create two services:

- Mongodb service listening on port 27017
- Flask server listening on port 8080

## Documentation
Project uses flask_restx to generate REST API documentation. You just need to access to:

http://localhost:8080/





