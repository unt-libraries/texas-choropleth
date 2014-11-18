# Texas Choropleth

A Django project for creating and sharing interactive choropleths maps of the state of Texas.

Dependencies:

* Python 2.7
* npm

## Quickstart

If you are just are interesting in taking this project for a test drive. 

1. Install [Docker](http://docker.com)
2. Install [fig](http://fig.sh)

3. Clone the repository and enter the project directory and touch `secrets.json`
 
    ```sh
    $ git clone https://github.com/unt-libraries/texas-choropleth.git
    $ cd texas-choropleth
    $ touch secrets.json
    ```
4. Add the following to `secrets.json`

    ```json
    {
      "SECRET_KEY": "your-super-secret-key-here"
    }
    ```

5. Run

    ```sh
    $ fig build
    ```

    This will pull down the MySQL and Python images and build the web image from the Dockerfile.
    
6. Run 

    ```sh
    $ fig run --rm web fab build_dev
    ```
    This will build the application.

7. Run 

    ```sh
    $ fig run --rm web fab manage:createsuperuser
    ```

8. Run 

    ```sh
    $ fig up -d
    ```
    This brings up the web and database containers and starts the application.

8. Navigate to `<dockerhost>:8000` and start using the app.

## Host your own
### Installation

__Note__: Configuring the web server and database is outside scope of the following instructions.

1. Clone the repository

    ```sh
    $ git clone https://github.com/unt-libraries/texas-choropleth.git
    ```

2. Create a virtualenv

    ```sh
    $ virtualenv ENV
    ```

3. Activate the virtualenv then enter the project directory

    ```sh
    (ENV)$ source ENV/bin/activate
    (ENV)$ cd texas-choropleth
    ```
4. Install the project dependencies

    ```sh
    (ENV)$ pip install -r requirements.txt
    ```

#### Pre-build

__Before you build the project, you must define a `secrets.json` file in side the project root.__ 

```sh
(ENV)$ touch secrets.json
```

The `local.py` settings only uses the `SECRET_KEY`, as the database settings preconfigured to work with Fig/Docker, but the `production.py` settings file also requires that the database settings are included.

Here is an example of what the `secrets.json` file should look like.

```json
{
  "FILENAME": "secrets.json",
  "SECRET_KEY": "some-super-secret-key",
  "DB_NAME": "texas_choropleth",
  "DB_USER": "your_db_user",
  "DB_PASSWORD": "your_db_password",
  "DB_HOST": "db",
  "DB_PORT": "3306",
  "EMAIL_HOST": "your.email.host",
  "EMAIL_PORT": "",
  "EMAIL_HOST_USER": "user",
  "EMAIL_HOST_PASSWORD":, "password",
  "EMAIL_USE_TLS": "",
  "EMAIL_USE_SSL": "",
}
```

#### Building

Run 

```sh
(ENV)$ fab build_prod
```

in the project root. (The same directory where `fabfile.py` is)

What will this do?

- Sync the database
- Run all the database migrations
- Download and install the front end libraries
- Load the data fixtures
- Collect the staticfiles

Then run 

```sh
(ENV)$ ./src/manage.py createsuperuser 
```

to create a site administrator

#### Important locations

__Static__ files will be at `<project_root>/src/static_final`

__Media__ files will be at `<project_root>/src/media`


## Development

#### Environment

See Quickstart

#### Running Tests

There is a fabric task for this. If using Fig and Docker:

```sh
$ fig run --rm web fab run_tests
```
to run all tests

To run app specific tests

```sh
$ fig run --rm web fab run_tests:<app-name>
```

