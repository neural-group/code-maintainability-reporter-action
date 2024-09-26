# install
.PHONY: install
install:
	rye pin 3.12
	rye sync

.PHONY: run_main
run_main:
	python -m code_maintainability_reporter_action.__init__

.PHONY: test
test:
	rye run pytest tests
