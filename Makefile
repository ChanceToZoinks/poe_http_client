TEST_DIR ?= ./tests

PYTEST_ARGS ?= -vvl

.PHONY: test
test:
	pytest $(PYTEST_ARGS) $(TEST_DIR)

.PHONY: test_builds
test_builds:
	pytest $(PYTEST_ARGS) $(TEST_DIR)/test_builds.py

.PHONY: test_economy
test_economy:
	pytest $(PYTEST_ARGS) $(TEST_DIR)/test_economy.py
