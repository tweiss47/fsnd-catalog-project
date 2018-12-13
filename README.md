# Catalog Project

| | |
| --- | --- |
| Author | Taylor Weiss |
| Date | November 2018 |

## Overview

The calalog project is a website and api that uses a database to present and
maintain an catalog of items which belong to different categories.

I've decided to use songs and music genres as the items and categories
respectively.

## Setup

Songcat is a flask application. There is a binary distribution available
under the dist directory, `songcat-0.1.1-py3-none-any.whl`. Installation
of the package was tested using a virtual environment. The following
commands were used:

```
python3 -m venv venv
pip3 install dist/songcat-0.1.1-py3-none-any.whl
```

The application should also run from the source directory without installing
as well, but following modules need to be available:

* flask
* flask_sqlalchemy
* google-auth
* requests

## Running the Server

Set the following environment variable to run the project using the `flask`
command in development mode.

```
FLASK_APP=songcat
```

To initialize the database run `flask init-model`. This will drop tables and
recreate the database schema.

To load the database with some test data run `flask init-test-data`.

Start the flask server using `flask run`.

## Implementation Notes

There are a couple of ways in which Songcat differs from the course
exercises.

First, it doesn't run directly from a script but uses the flask module and
application factory structure. The [flask
tutorial](http://flask.pocoo.org/docs/1.0/tutorial/) was used as a model to
structure the project.

Second, the project requirements included adding an external authentication
provider. Google signin was used for this. But local accounts were also used
to make the initial setup and testing easier.

Third, I used the flask_sqlalchemy module. It seemed like a better way to
handle sessions.

Finally, I have had trouble running vagrant VMs on my laptop as it there are
hyper-v policy settings that keep getting in the way. So the project was not
built and tested in the vagrant vm environment. However I did test deploying
the package to linux environment and built the separate distribution to make
the deployment of dependencies easier.

## Feature Notes

I believe this has all the required elements. Create, Read, Update, Delete
are all supported. Browsing by category and most recent entry is provided.
A read only API is provided for retreiving songs at `api/song` and reading
songs by id `api/song/1`. I added routes and verbs with the idea of
supporting all CRUD operations in the API, but was running behind schedule.
The UX sticks fairly close to the sample screen shots.
