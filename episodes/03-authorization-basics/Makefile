PY ?= python3
ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SHARED := $(abspath $(ROOT)../../shared)

.PHONY: help lab-up-native lab-down-native stop-http-demo start-http-demo status verify-lab test clean-run

help:
	@echo "Episode 03 — Authorization basics (127.0.0.1 only)"
	@echo "  make lab-up-native     Start shared training-app :5050 and http-demo :8080"
	@echo "  make status            Show managed PIDs and probes"
	@echo "  make verify-lab        Confirm health + demo"
	@echo "  make stop-http-demo    Stop ONLY managed http-demo"
	@echo "  make start-http-demo   Start/restart ONLY http-demo"
	@echo "  make lab-down-native   Stop both managed services"
	@echo "  make test              Run this episode's unittest suite"
	@echo "  make clean-run         Clear shared .run metadata"

lab-up-native:
	@$(PY) $(SHARED)/labctl.py up

lab-down-native:
	@$(PY) $(SHARED)/labctl.py down

stop-http-demo:
	@$(PY) $(SHARED)/labctl.py stop-demo

start-http-demo:
	@$(PY) $(SHARED)/labctl.py start-demo

status:
	@$(PY) $(SHARED)/labctl.py status

verify-lab:
	@$(PY) $(SHARED)/labctl.py verify

test:
	@$(PY) -m unittest discover -s $(ROOT)tests -v

clean-run:
	@rm -rf $(SHARED)/.run
	@echo "Cleared shared/.run/"
