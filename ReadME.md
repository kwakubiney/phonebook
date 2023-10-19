## Setting up

1. Create a virtual environment and run `pip install -r requirements.txt`

1. Create a `.env` file in the root of the project with the following variables;
    - `POSTGRES_NAME`
    - `POSTGRES_PASSWORD`
    - `POSTGRES_PORT`
    - `POSTGRES_DB`
    - `POSTGRES_HOST`

2. Run `python3 manage.py makemigrations` and `python3 manage.py migrate` to create database tables.

3. Run `python3 manage.py runserver` to run the HTTP server

