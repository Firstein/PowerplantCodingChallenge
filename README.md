# Powerplant Coding Challenge

Coding Challenge: https://github.com/gem-spaas/powerplant-coding-challenge

Build a REST API exposing an endpoint `/productionplan` that accepts a POST
more info in the link above 

## How to build and launch the app

### With flask

To build the app directly with flask, it is advise to use a virtual environment.
Install the dependencies with pip:
```
python pip install -r requirements.txt
```
Then start the app with flask:
```
flask run
```

### With Docker

To build the app using docker, first build the image:
```
docker build -t powerplant-coding-challenge .
```
Then run it:
```
docker run -p 8888:8888 -w /app -v "$(pwd):/app" powerplant-coding-challenge
```
On windows:
```
docker run -p 8888:8888 -w /app -v "/c/<path_to_app>:/app" powerplant-coding-challenge
```

## Co2 emission allowances

Co2 emission allowances can be taking into account or not
by setting in the app.py file the `C02_ALLOWANCES` to `True` (activate) or `False` (deactivate)
A config file would be better but time was lacking...
