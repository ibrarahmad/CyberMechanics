.PHONY: help test test-01 test-02 test-03 test-04 status down

help:
	@echo "Cyber Mechanics — educational local labs (127.0.0.1 only)"
	@echo "  make test       Run all episode test suites"
	@echo "  make test-01    Episode 01 only"
	@echo "  make test-02    Episode 02 only"
	@echo "  make test-03    Episode 03 only"
	@echo "  make test-04    Episode 04 only"
	@echo "  make status     Shared lab status (episodes 02–04 runtime)"
	@echo "  make down       Stop shared lab services"
	@echo ""
	@echo "Episodes:"
	@echo "  cd episodes/01-your-first-local-lab && make help"
	@echo "  cd episodes/02-nmap-local-port-scan && make help"
	@echo "  cd episodes/03-authorization-basics && make help"
	@echo "  cd episodes/04-safer-sql-queries && make help"

test: test-01 test-02 test-03 test-04
	@echo "ALL EPISODE SUITES PASSED"

test-01:
	@$(MAKE) -C episodes/01-your-first-local-lab test

test-02:
	@$(MAKE) -C episodes/02-nmap-local-port-scan test

test-03:
	@$(MAKE) -C episodes/03-authorization-basics test

test-04:
	@$(MAKE) -C episodes/04-safer-sql-queries test

status:
	@python3 shared/labctl.py status

down:
	@python3 shared/labctl.py down
