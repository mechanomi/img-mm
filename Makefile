APP_NAME    := imgmm
TOP_DIR     := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
SRC_DIR     := $(TOP_DIR)/src
VENV_DIR    := $(TOP_DIR)/.venv
BIN_DIR     := $(VENV_DIR)/bin
ACTIVATE    := $(BIN_DIR)/activate
PYTHON      := python3.7
PIP         := $(PYTHON) -m pip
FLAKE8      := $(BIN_DIR)/flake8
FLAKE8_ARGS := --count --show-source --max-complexity=8 --statistics
BLACK       := $(BIN_DIR)/black
BLACK_ARGS  := --line-length 79

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
	    $(PYTHON) -m pip install --upgrade -r requirements.txt

$(BLACK): $(ACTIVATE)
	. $(ACTIVATE) && \
	    $(PYTHON) -m pip install --upgrade -r requirements.txt

.PHONY: test
test: $(FLAKE8) $(BLACK)
	. $(ACTIVATE) && \
	    $(FLAKE8) $(FLAKE8_ARGS) $(SRC_DIR)
	. $(ACTIVATE) && \
	    $(BLACK) $(BLACK_ARGS) --check $(SRC_DIR)

reformat:
	. $(ACTIVATE) && \
	    $(BLACK) $(BLACK_ARGS) $(SRC_DIR)


.PHONY: dev
dev:
	@ if test ! -d "$(DIR)"; then \
	    echo "You must set the DIR variable to a directory"; \
	    false; \
	fi
	. $(ACTIVATE) && \
	    $(PYTHON) -m pip install -e .
	. $(ACTIVATE) && \
	    cd "$(DIR)" && \
	    FLASK_ENV=development \
	    FLASK_APP=$(APP_NAME) \
	    flask run
