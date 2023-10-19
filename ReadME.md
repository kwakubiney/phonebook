## Setting up

1. Create a `.env` file in the root of the project with the following variables;
    - `POSTGRES_NAME`
    - `POSTGRES_PASSWORD`
    - `POSTGRES_PORT`
    - `POSTGRES_DB`
    - `POSTGRES_HOST`

2. Run `python3 manage.py makemigrations` and `python3 manage.py migrate` to create database tables.