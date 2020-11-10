# Timetable Scheduler [WIP]

## Setting up a development environment

We assume that you have `git` and `pip` installed ([ref](https://packaging.python.org/guides/installing-using-linux-tools/#arch-linux) )

1. Clone the code repository 
```
    git clone https://github.com/adiMallya/timetable-scheduler.git && cd timetable-scheduler
```
2. Install the dependencies from the `requirements.txt` file
```
    pip install -r requirements.txt
```

## Running the app

```
    export FLASK_APP=run.py
    flask run
```
Alternatively you can use python -m flask:

```
    export FLASK_APP=run.py
    python -m flask run
```
Point your web browser to http://localhost:5000/