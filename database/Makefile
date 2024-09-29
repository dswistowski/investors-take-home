WORKDIR = $(shell pwd)

SEED_FILE ?= $(shell pwd)/seed.csv
DB_URL ?= postgresql://investors:password@localhost/investors

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

validate: check typecheck ## run linter and typechecker



check:  ## check code using linter
	poetry run ruff check .

typecheck:  ## check the types with mypy
	poetry run mypy . --enable-incomplete-feature=NewGenericSyntax

format:  ## reformat code using linter
	poetry run ruff format .
	poetry run ruff check . --fix

install-dev:
	poetry install --with=dev

migrate-db:  ## run db-migrations
	$(if $(shell command -v liquibase  2>/dev/null),,$(error Please install liquibase with 'brew install liquibase' or use docker compose: 'make migrate-db-docker))
	liquibase --search-path=. --changelog-file changelog.yml --username investors --password=password --url jdbc:postgresql://localhost:5432/investors update

seed:  ## load example data to the database
	DB_URL=$(DB_URL) SEED_FILE=$(SEED_FILE) poetry run python -m seed

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
        match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
        if match:
                target, help = match.groups()
                print("%-30s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

