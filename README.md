# Phone Book API Server #

This folder contains a template of a RESTful API service served on a web server. It uses a uvicorn server, written in
Python with the FastAPI framework.

### Assumptions and Instructions ###
1. I used a postgreSQL database for this project,
I buried its URL in the .env file in the phone_book_api_server folder, under an environment variable named `DATABASE_URL`, to enable interfacing with the database you must do this as well, this is the template for the url:
postgresql:///?user={user}&password={password}&database={database}&host={host}&port={port}

2. In terms of necessary records for the table, I assumed that phone number first name and last name are necessary, while email is optional.
3. I used Python's phonenumbers library to perform validation on phone numbers, note that this is the proper format in Israel: +972********* (9 digits after the prefix).
4. Also, to enter the other parameters, pay attention to the correctness of the email address, alphabetical names, etc.
5. To build the docker, in Terminal write in Dockerfile path: `docker build -t phonebook-api:latest .`
After the build has finished, write in Terminal :` docker run -p 8080:8000 phonebook-api:latest `
6. Finally, the system can be triggered by Postman, however,
It is more than recommended to use `FastAPI's Swagger`, which allows a convenient and easy visual interface for the user!
To reach it, after running the system, go to localhost:8000/docs.

## How do I get set up? ##

### Install Python and Poetry ###

You can download the Python installer from the Python site's [downloads page](https://www.python.org/downloads/).

Poetry is a Python packaging and dependency management tool. To install it, please follow the instructions
in [Poetry's documentation](https://python-poetry.org/docs/#installation). It is strongly recommended using the `curl`
installing method.

For optimal results, make sure you install the following versions:

* **Python**: >=3.9.6, <3.10.0
* **Poetry**: >=1.4.2

By default, poetry creates all its virtual environments in a fixed dedicated directory on the local computer. It is
recommended to change this behavior, and make poetry create a virtual environment for each project in its root directory
in a directory named `.venv`. this is done with the following command (needed to be run only once after poetry's
installation):

```sh
poetry config virtualenvs.in-project true
```


### Clone this repository ###

Go to the [Templates home page](https://github.com/atayziv/PhoneBookAPI/tree/main) in github, click on the Code
button in the top right corner, and copy the `git clone` command to clone this repository wherever you want.


### Install dependencies ###

Run the following command (and all poetry's commands) in the app's root folder:

```sh
poetry install
```

* It creates a virtual environment with all the packages detailed in the `pyproject.toml` file, in the dependencies
  sections.
* After that, all the commands that depends on the installed packages should be run from inside this virtual
  environment. To do that, simply run `poetry shell`, and make sure the virtual environment's directory name is written
  in the beginning of the terminal command.

### Start application in development mode ###

The following command runs the app in the development mode (don't forget to run it in the virtual environment):

```sh
python phone_book_api_server
```

After that, the server will be available on port 8000 of the local machine.

### Run tests ###

The following command runs all the app's tests, linters and security checks (don't forget to run it in the virtual
environment):

```sh
tox
```

## Project's structure explained ##

### `phone_book_api_server` ###

Contains all the source code files, written in Python files (`*.py`).

#### `api` ####

* Contains all the server's services.
* `server.py` is the main file that spin's up the FastAPI instance and calls all the routers.

##### `routers` ######

* Contains all the server's routers.
* Each router should always contain as few logic as possible. All the routers specific logic are placed in a
  matching service,`contact_service`  from the `services` folder.

##### `static` ######

* Contains the static web files (JavaScripts and CSS) needed to serve the swagger docs.

#### `data_models` ####

* Contains the shape definitions (=interfaces) of the objects used in the app.
* All the models are extend the `SharedBaseModel` class.

#### `exceptions` ####
* Contains all the custom exceptions that created to match edge cases.

#### `database` ####
* The database folder contains SQLAlchemy model definitions for the application's database tables.

#### `clients` ####

* Contains all the accesses to external services and data needed for the `contact_service`.

#### `services` ####

* Contains all the logic needed for the routers.

#### Files in `fastapi_server`'s root ####

* `__main__.py`: The entry point of the app when it is run locally for development purposes.
* `config.yaml`: The app's main configuration file.
* `constants.py`: The app's main constant settings.
* `containers.py`: All the dependencies that should be injected to the app.

### `tests` ###

Contains all the tests code files, written in Python files (`*.py`), with the pytest framework. For more information,
please check [pytest's documentation](https://docs.pytest.org/).

#### `test_data` ####

Contains all the files needed for the tests.

#### `unit` ####

Contains all the unit tests, arranged in folders corresponding to the source code's hierarchy.

### `.coveragerc` ###

Configuration file of the `coverage` library. For more information, please
check [Coverage's documentation](https://coverage.readthedocs.io/en/coverage-5.5/config.html).

### `.dockerignore` + `Dockerfile` ###

Files used for deploying the app in production.


### `README.md` ###

This file :)

### `poetry.lock` + `pyproject.toml` ###

Configuration files of the project with Poetry.

`pyproject.toml` contains general info about the project,the dependencies of the project and more tools' configurations.

`poetry.lock` is auto-generated and should be committed. It should not be modified manually.

### `tox.ini` ###

Configuration file of Tox. 

