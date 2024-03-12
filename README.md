# shorturl
Python web api for shortening urls. Uses celery for persisting newly created urls.

## Tech stack
* FastAPI `0.110.0`
* SQLAlchemy `2.0.28`
* Alembic `1.13.1`
* PostgreSQL `16.2`
* Docker
* Celery

## Functionality
SwaggerUI docs available at `localhost:8000/docs`

## Setup
1. Clone repository:
`$ git clone https://github.com/amadeuszklimaszewski/shorturl.git`
2. Run in root directory:
`$ make build-dev`
3. Run template: `$ make up-dev`


## Migrations
Run `$ make makemigrations` to create migrations file.
Run `$ make migrate` to apply migration files in database.


## Tests
`$ make test`


## Makefile
`Makefile` contains useful command aliases
