# SOSE

***
The Simple Online Store Engine based on the Flask framework.

## Install

***

Clone the git repository

```
$ git clone https://github.com/dudilona/sose
$ cd sose
```

Create a virtualenv and activate it:

```
$ python3 -m venv venv
$ . venv/bin/activate
```

Or on Windows cmd:

```
> py -3 -m venv venv
> venv\Scripts\activate.bat
```

Install SOSE:

```
$ pip install -e .
```

## Run

***

```
$ export FLASK_APP=src
$ export FLASK_ENV=development
$ flask init-db
$ flask run
```

Or on Windows cmd:

```
> set FLASK_APP=src
> set FLASK_ENV=development
> flask init-db
> flask run
```

Open http://127.0.0.1:5000 in a browser.