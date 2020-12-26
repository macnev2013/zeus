VENV_DIR ?= .venv
PIP_CMD ?= pip

ifeq ($(OS), Windows_NT)
	VENV_RUN = . $(VENV_DIR)/Scripts/activate
else
	VENV_RUN = . $(VENV_DIR)/bin/activate
endif

setup-venv:
	(test `which virtualenv` || $(PIP_CMD) install --user virtualenv) && \
		(test -e $(VENV_DIR) || virtualenv $(VENV_OPTS) $(VENV_DIR))

install-venv:
	make setup-venv && \
		test ! -e requirements.txt || ($(VENV_RUN); $(PIP_CMD) -q install -r requirements.txt)


install:
	(make install-venv) || exit 1

run:             ## Manually start the local infrastructure for testing
	($(VENV_RUN); flask db init; flask db migrate -m "Initial migration."; flask db upgrade;flask run)

clean:             ## Clean up (npm dependencies, downloaded infrastructure code, compiled Java classes)
	rm -rf $(VENV_DIR)
