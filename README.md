# cornerCase
## Table of contents
* [General info](#general-info)
* [Features](#features)
* [Technologies](#technologies)
* [Setup](#setup)
* [API Documentation](#api-documentation)

## General info
Company needs internal service for its’ employees which helps them to make a decision
on lunch place. Each restaurant will be uploading menus using the system every day over
API and employees will vote for the menu before leaving for lunch.
The solution can be presented in the Docker environment, which will add additional Karma
points.	
## Features
● There should be an API for:

○ Authentication

○ Creating restaurant

○ Uploading menu for restaurant (There should be a menu for each day)

○ Creating employee

○ Getting current day menu

○ Voting for restaurant menu

○ Getting results for the current day. The winner restaurant should not be the
winner for 3 consecutive working days

○ Logout
## Technologies
Project is created with:
* Python3
* Django Rest Framework
* SQLite

## Setup
To run this project, locally using docker:

```
$ sudo docker-compose down
$ sudo docker-compose build
$ sudo docker-compose up --detach
```
## API Documentation
I have Created API Documentation using Postman:

Default Admin-

username: admin

password: admin@cornerCase

https://documenter.getpostman.com/view/1175682/UUy3ASqD#2bd1b40a-81f5-9c07-857b-9f01015401ce