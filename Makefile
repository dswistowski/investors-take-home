WORKDIR = $(shell pwd)

.PHONY: backend

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


migrate-db:  ## run db-migrations
	$(MAKE) -C database migrate-db

seed:  ## run db-seed
	$(MAKE) -C database seed

backend: ## run backend service
	$(MAKE) -C backend start

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
        match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
        if match:
                target, help = match.groups()
                print("%-30s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

