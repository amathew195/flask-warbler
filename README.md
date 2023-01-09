# Warbler

Warbler is a full stack web application of a Twitter clone site. Logged in users can create new messages(posts) and share with followers.
Users are also able to like/unlike posts and follow/unfollow other users.

Deployed app can be found [here](https://warbler-qav5.onrender.com).

# Table of Contents
1. [Features](#Features)
2. [Tech stack](#Tech-stack)
3. [Database Entity Relationships](#Database-entity-relationships)
4. [Install](#Install)
5. [Testing](#Testing)
6. [Deployment](#Deployment)
7. [Future features](#Future-features)
8. [Contributers](#Contributers)

## Features<a name="Features"></a>:
* Utilizes RESTful API
* Users must create an account to access the application. A valid email is not required, but passwords are hashed and authenticated using bcrypt.
* Proper authorization checks are in place to ensure only logged in users have access to specific pages.
* Logged in users can search for people and follow or unfollow them.
* Logged in users can posts messages.
* Logged in users can can like or unlike messages.
* Logged in users can edit their own profile.

## Tech stack<a name="Tech-stack"></a>:

### Backend:
![alt text](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white&style=for-the-badge)
![alt text](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=for-the-badge)

### Frontend:
![alt text](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![alt text](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![alt text](https://img.shields.io/badge/-Bootstrap-7952B3?logo=bootstrap&logoColor=white&style=for-the-badge)

### Database Management:
![alt text](https://img.shields.io/badge/-PostgresSQL-4169E1?logo=postgresql&logoColor=white&style=for-the-badge)
![alt text](https://img.shields.io/badge/-SQLAlchemy-F40D12?logo=sqlalchemy&logoColor=white&style=for-the-badge)

## Database Entity Relationships<a name="Database-entity-relationships"></a>:
![alt text](https://github.com/amathew195/flask-warbler/blob/main/images/Warbler%20-Entity%20Relationship%20Diagram.jpeg?raw=true)
