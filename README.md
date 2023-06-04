# Backend Test

## Description

The product department wants a system to be notified when a customer requests assistance from a bot. The bot will make an http call (like a webhook) with the following information:

- Topic: a string with values can be sales or pricing
- Description: a string with a description of the problem that needs assistance from.

You need to expose an API endpoint that will receive this call and depending on the selected topic will forward it to a different channel:

``` 
Topic    | Channel   
----------------------
Sales    | Slack
Pricing  | Email
```

## Notes:
- Slack and Email are suggestions. Select one channel that you like the most, the other can be a mock.
- There may be more topics and channels in the future.

## The solution should:
- Be written in your favorite language and with the tools with which you feel comfortable.
- Be coded as you do daily (libraries, style, testing...).
- Be easy to grow with new functionality.
- Be a dockerized app.


---
![ci workflow](https://github.com/aritztg/backend-test/actions/workflows/quality_check.yml/badge.svg)

## Approach

> _The only line that never fails, is the one we never write._

Given the problem, I chose to use fastAPI to expose a simple REST API, because of its concurrency and speed, and
because of how well it fits for the requirements. With a minimum amount of code, no bloat, and good practises as
type hinting and docstrings, we can also expose a swagger documentation in `/docs` and/or `/redoc` paths.

Normally I would choose Django for mostly any kind of web project, but I felt it is too big and bloated for just an
API. Given that it is not mandatory to persist any object in the DB (sure this could be another endpoint), but this is
not the case for now. Going with FastAPI, one could persist data into DB with something like
[TortoiseORM](https://tortoise.github.io/) (good performance and heavily inspired in Django's ORM, so pretty familiar).


## Installation

This guide assumes that the reader has a minimal experience with python and its virtualenvs.

1. Install a python version (this was tested with 3.11.3): `$ pyenv install 3.11.3`. If `pyenv` is not available in
   your OS, you can use `virtualenv` (`poetry` would require different steps).
2. Create a virtualenv: `$ pyenv virtualenv 3.11.3 landbot-backend`
3. If not already, now you can start using that environment: `$ pyenv activate landbot-backend`
4. Install dependences: `$ pip install -r requirements.txt`
5. (Optional) Install dev dependences (for linting and such): `$ pip install -r requirements-dev.txt`
6. Fill credentials in `.env` file. Do not use double quotes or whitespaces.
7. Execute the cli app. `$ python app/backend.py`

## How to run

### Locally

As a regular python app (in the right environment):
```bash
$ python app/backend.py
```

or using makefile entrypoint:

```bash
$ make run
```

Then you should be able to access [http://0.0.0.0:80/docs] and play around with the exposed endpoint. If you prefer,
you can also check docs via [http://0.0.0.0:80/redoc] UI.

### Docker

First build the image (read the file first to understand what it does):
```bash
$ docker build -t backend-test-image .
```

Then you can run a container based on that image:
```bash
$ docker run -d --name backend-test-container -p 80:80 backend-test-image
```

## Further development
- Consider the use of pylama for more complete linting.
- Add some FastAPI middlewares, such HTTPSRedirectMiddleware, TrustedHostMiddleware.
- Integrate some logs/app monitor like Sentry or Datadog.
- Ideally, we must ensure async libraries to perform the final operations (ie, Email sending, DB insertion, etc) so we
don't block the thread during its processing.
- Ideally, in a HA environment, the output of this microservice should go to some queue system, having workers
processing them and some long enough retention policy in those subscriptions.
- Using Github actions, check linters and go further (staging/deploy) only if certain threshold has been met (done).

### Linters
Please ensure you have installed development dependences first: `$ pip install -r requirements-dev.txt`.

#### Ruff
Very fast linter, but still does not have the same amount or rules available in pylint. It would be perfect to be used
in a pre-commit Git hook. Uses `pyproject.toml` as configuration file.
```bash
ruff check .
```

#### Pylint
It uses the configuration `pylintrc` settings file. No rules were disabled, AFAIK. It takes more time with larger
codebases. It can be executed locally, and tipically in CD/CI pipelines instead of ruff (because of its large amount
of rules), making the pipeline failing if a minimum threshold score is not reached.
```bash
$ pylint $(find . -name "*.py")

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

#### Isort
Not exactly a linter, but a useful tool anyway. It ensures some guide styling in regards of module imports.
```bash
$ isort .
```

### Tests
Ensure you install dev-requirements first. Then simply execute:
```bash
$ python -m unittest discover
```

### Makefile
You can run (you need to be in the right virtualenv first):
```bash
make run
make tests
make lint
```

### Github actions
A Github action has been added (`.github/workflows/quality_check.yml`) to check pylint over all py files in the
`main` branch. If linter score is higher than `9`, it could continue to the next ci/cd step (undefined).