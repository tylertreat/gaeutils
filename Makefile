SHELL := /bin/bash
PYTHON := python
PIP := pip

BUILD_DIR := .build

all: deps

clean:
	find . -name "*.py[co]" -delete

distclean: clean
	rm -rf $(BUILD_DIR)
	rm -rf $(LIBS_DIR)

deps: clean py_deploy_deps py_dev_deps

integrations:
	nosetests --logging-level=ERROR -a slow --with-coverage --cover-package=gaeutils

py_deploy_deps: $(BUILD_DIR)/py_deploy_deps.out

py_dev_deps: $(BUILD_DIR)/py_dev_deps.out

test: deps integrations

unit:
	nosetests

$(BUILD_DIR)/py_deploy_deps.out: requirements.txt
	@mkdir -p .build
	$(PIP) install -Ur $< && touch $@

$(BUILD_DIR)/py_dev_deps.out: requirements_dev.txt
	@mkdir -p .build
	$(PIP) install -Ur $< && touch $@
