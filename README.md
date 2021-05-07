<h1 align="center">timeUp</h1></br>

<br>
<p align="center">
Finding it hard to manually manage all your schedules ? If your given to setup timetables at your college, why try hard ? :sweat: Lets automate it !:open_mouth: <br>
<img width="320px" src="tt_scheduler/static/images/logo-1.png" alt="timeUp logo"></img>
</br> timeUp is your saviour. Just feed in the details and let it time it <em>Up</em> :wink: for you!
</p><br>


## Quicksetup :heavy_check_mark:

We assume that you have `git` and `pip` installed ([ref](https://packaging.python.org/guides/installing-using-linux-tools/#arch-linux))

1. Clone the code repository 
```
    git clone https://github.com/adiMallya/timetable-scheduler.git && cd timetable-scheduler
```
2. Install the dependencies from the `requirements.txt` file
```
    pip install -r requirements.txt
```
3. Create a `timetable-scheduler/instance/config.py` file

    Set your app's secret key and database url as environment variables. For example, add the following to `instance/config.py`
```
    SECRET_KEY = 'something-really-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///example.db'
```

## Running the app

```
    export FLASK_CONFIG=development
    export FLASK_APP=run.py
    set FLASK_DEBUG=1
    flask run -h localhost -p 5000
```
On Windows, you could use CMD or Anaconda Shell :

```
    set FLASK_CONFIG=development
    set FLASK_APP=run.py
    set FLASK_DEBUG=1
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


## Deployment :question:

In your production environment, make sure the environment variable FLASK_CONFIG is set to "production" or FLASK_DEBUG is unset, so that ProductionConfig is used, and set DATABASE_URL as per your production needs.


## ⚠️ Note

This project was part of an assignment and hence is for learning purposes only.
