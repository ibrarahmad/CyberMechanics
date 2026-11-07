PY ?= python3
ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: help lab-up-native lab-down-native stop-http-demo start-http-demo status verify-lab test clean-run start stop restart-demo

help:
	@echo "Episode 01 — Your First Local Lab (127.0.0.1 only)"
	@echo "  make lab-up-native     Start training-app :5050 and http-demo :8080"
	@echo "  make status            Show managed PIDs and probes"
	@echo "  make verify-lab        Confirm /health JSON and demo HTML"
	@echo "  make stop-http-demo    Stop ONLY the managed http-demo on :8080"
	@echo "  make start-http-demo   Start/restart ONLY http-demo"
	@echo "  make lab-down-native   Stop both managed services"
	@echo "  make test              Run unittest suite (starts/stops its own lab)"
	@echo "  make clean-run         Remove .run metadata (does not kill foreign PIDs)"
	@echo "Aliases: make start | stop | restart-demo"

lab-up-native:
	@$(PY) $(ROOT)labctl.py up

lab-down-native:
	@$(PY) $(ROOT)labctl.py down

stop-http-demo:
	@$(PY) $(ROOT)labctl.py stop-demo

start-http-demo:
	@$(PY) $(ROOT)labctl.py start-demo

status:
	@$(PY) $(ROOT)labctl.py status

verify-lab:
	@$(PY) $(ROOT)labctl.py verify

test:
	@$(PY) -m unittest discover -s $(ROOT)tests -v

clean-run:
	@rm -rf $(ROOT).run
	@echo "Cleared .run/"

# Friendly aliases (same as primary targets)
start: lab-up-native
stop: lab-down-native
restart-demo: start-http-demo
