TEST_DIR ?= ./tests

PYTEST_ARGS ?= -vvl
PYTEST_CMD ?= pytest --cov=ninjaclient --cov=apiclient

.PHONY: test
test:
	$(PYTEST_CMD) $(PYTEST_ARGS) $(TEST_DIR)

.PHONY: test_builds
test_builds:
	$(PYTEST_CMD) $(PYTEST_ARGS) $(TEST_DIR)/test_builds.py

.PHONY: test_economy
test_economy:
	$(PYTEST_CMD) $(PYTEST_ARGS) $(TEST_DIR)/test_economy.py
