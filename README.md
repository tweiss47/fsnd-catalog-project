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

## Startup

Set the following environment variables to run the project using the `flask`
command in development mode.

```
FLASK_APP=songcat
FLASK_ENV=development
```

To initialize the database run `flask init-model`. This will drop tables and
recreate the database schema.

To load the database with some test data run `flask add-test-data`.

Start the flask server using `flask run`.

## Project Features

## Notes on the Code

