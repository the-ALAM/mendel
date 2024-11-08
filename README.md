# Features

- pep8 compliant
- scheduled ETL processes
- integration with FHIR-compatible databases/APIs
- data validation
- logging for better monitoring and observability
- error handling
- parallelization-capable
- incremental-loading (WIP)

---

# Instructions

## Environment

- make sure you have [docker](https://docs.docker.com/desktop/install/windows-install/) installed
- make sure you have [docker-compose](https://docs.docker.com/compose/install/) installed
- make sure you have [python](https://www.python.org/downloads/) 3.9 installed 
- make sure you have the requirements.txt installed

- Create a `.env` file in the root directory with the following content:

- `POSTGRES_HOST`: the host of the PostgreSQL database
- `POSTGRES_PORT`: the port of the PostgreSQL database
- `POSTGRES_DB`: the name of the PostgreSQL database
- `POSTGRES_USER`: the username of the PostgreSQL database
- `POSTGRES_PASSWORD`: the password of the PostgreSQL database

example:

```bash

POSTGRES_HOST={your-host}
POSTGRES_DB={your-db}
POSTGRES_USER={your-user}
POSTGRES_PASSWORD={your-password}
POSTGRES_PORT={your-port}

```

## data prep

- unzip `data/patients_fhir_100.zip`

## Docker

- run `docker build -t mendel/app .` to build the app image
- run `docker-compose up --build` to build and run the container
- that's it! you're all set.
- you can use `psql -h localhost -d mendel -U mendel -p 5432` in the database container terminal to connect to the database
- `\dt`
- `select * from information_schema.tables;`
- ...

<!-- - Run `docker-compose exec mendel python -m pytest` to run the tests
- Run `docker-compose exec mendel python -m pytest --cov-report=html` to run the tests and generate an HTML coverage report -->


## Local

- `pip install -r requirements.txt`
- run `python scheduler.py` to run the scheduler, you can select the interval and time from `main.py`
- run `python main.py` to run the whole project with the scheduled ETL processes
- run `python processor.py` to run the data extraction and transformation logic and update the CSV files in `out/`
- run `python loader.py` to run the data loading logic and upload the CSV files to the database

<!-- - `python -m pytest` -->

---

# Database Schema

![schema](resources/database_schema.png)

---

# Technologies

- [Synthea](https://github.com/synthetichealth/synthea)
- [FHIR](https://www.hl7.org/fhir/)
- [json crack](https://github.com/AykutSarac/jsoncrack.com)
- [Pandas](https://pandas.pydata.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [Pytest](https://docs.pytest.org/en/7.1.x/)
- [Docker](https://www.docker.com/)
- [scheduler](https://pypi.org/project/schedule/)
