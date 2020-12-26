# Timetable Scheduler [WIP]

## Setting up 

We assume that you have `git` and `pip` installed ([ref](https://packaging.python.org/guides/installing-using-linux-tools/#arch-linux) )

1. Clone the code repository 
```
    git clone https://github.com/adiMallya/timetable-scheduler.git && cd timetable-scheduler
```
2. Install the dependencies from the `requirements.txt` file
```
    pip install -r requirements.txt
```
3. Create a `timetable-scheduler/instance/config.py` file to store keys(this is to be hidden in production/version control)

Inside the instance/config.py file
```
    SECRET_KEY = '842266388f2c6e4afc87a51854826973'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
```

## Running the app

```
    export FLASK_CONFIG=development
    export FLASK_APP=run.py
    flask run -h localhost -p 5000
```
On Windows, you could use CMD or Anaconda Shell :

```
    set FLASK_CONFIG=development
    set FLASK_APP=run.py
    flask run -h localhost -p 5000
```
Point your web browser to http://localhost:5000/



## Setting up database

```
    flask db init 
    flask db migrate
    flask db upgrade
```

Then each time the database ```models``` change repeat the ```migrate``` and ```upgrade``` commands.

- Skip first two steps if cloned repo has existing db.

- To sync the dB in another system just refresh the migrations folder from source control and run the upgrade command.

Read more about [Flask-Migrate](https://qxf2.com/blog/database-migration-flask-migrate/)