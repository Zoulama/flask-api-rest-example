# Kibaro user service

The User Service is a python 3 project that handles user data in a Mongo DB 

## Install python3
```
brew install python3
```
## Install pip
```
sudo easy_install pip
```
## Create and activate kibaro-user virtual environment
```
make setup
```
## Run kibaro-user locally
```
make up
```

[Head to]( http://localhost:8080)

## Update requirements.txt
```
pip freeze > requirements.txt
```

## Environment variables

|                Name | Description   |
|-------------------- |---------------|
| DB_MONGO_USERNAME   | Username      |
| DB_MONGO_PASSWORD   | Password      |
| DB_MONGO_HOST       | Hostname      |
| DB_MONGO_PORT       | Port          |
| DB_MONGO_URI_SCHEME | Scheme        |
| DB_MONGO_DATABASE   | Database name |


## Environments
| ENVIRONMENTS | URL                                                        |
|--------------|------------------------------------------------------------|
| DEV          | https://kibaro-user-svc-py-fjhmnd5asa-ew.a.run.app         |
| STAGING      | https://kibaro-user-svc-py-fjhmnd5asa-ew.a.run.app         |
| PRODUCTION   | https://kibaro-user-svc-py-fjhmnd5asa-ew.a.run.app         |
