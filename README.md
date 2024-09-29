# Starting project

To start project localy run:
```bash
docker compose up
```

# Starting project long version

## Starting db by hand

start local database (or use own and set it as DB_URL env variable):
```bash
docker compose up db
```

## Run db migration

Db migration use `liquibase` which can be installed locally with `brew install liquibase`
To run migration you need to call command:

```bash
liquibase --search-path=./database --changelog-file changelog.yml --username investors --password=password --url jdbc:postgresql://localhost:5432/investors update

```

please make sure if you using your local db, to update username, password and database url

It's possible to run migration with make file:

```bash
make migrate-db 
```

## Seed db with data from csv

To load data from csv file please run command in `database` directory:

```bash
export SEED_FILE=$(pwd)/seed.csv
export DB_URL=postgresql://investors:password@localhost/investors
poetry run python -m seed
```

You can use make file for it:
```bash
make seed
```


## Start backend
Go to backend directory and run command:

```bash
export DB_URL=postgresql://investors:password@localhost/investors
poetry run python -m uvicorn backend.app:app --host=0.0.0.0 --reload
```

There is make command:
```bash
make start-dev
```

