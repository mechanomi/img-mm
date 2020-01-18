SRC_DIR     := src
IMG_MM      := $(SRC_DIR)/img-mm.py
VENV_DIR    := .venv
BIN_DIR     := $(VENV_DIR)/bin
ACTIVATE    := $(BIN_DIR)/activate
PYTHON      := python3.7
PIP         := $(PYTHON) -m pip
FLAKE8      := $(BIN_DIR)/flake8
FLAKE8_ARGS := --count --show-source --max-complexity=8 --statistics

help:
	@echo "Options:"
	@echo
	@echo "- make dev DIR=<DIR>"
	@echo "- make test"

$(ACTIVATE):
	$(PYTHON) -m venv $(VENV_DIR)
	. $(ACTIVATE) && \
	    $(PIP) install --upgrade pip

$(FLAKE8): $(ACTIVATE)
	. $(ACTIVATE) && \
	    $(PYTHON) -m pip install --upgrade -r requirements-test.txt

.PHONY: test
test: $(FLAKE8)
	. $(ACTIVATE) && \
	    $(FLAKE8) $(SRC_DIR) $(FLAKE8_ARGS)

.PHONY: dev
dev:
	@ if test ! -d "$(DIR)"; then \
	    echo "You must set the DIR variable to a directory"; \
	    false; \
	fi
	. $(ACTIVATE) && \
	    $(PYTHON) -m pip install --upgrade -r requirements.txt
	. $(ACTIVATE) && \
	    FLASK_ENV=development $(PYTHON) $(IMG_MM) "$(DIR)"
