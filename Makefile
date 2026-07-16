.PHONY: help setup update status test-grmc install-grmc

ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
GRMC := $(ROOT)experiments/grmc
LAB_DATA := $(ROOT).lab_data/grmc

help:
	@echo "Grok-Workspace-main"
	@echo "  make setup         clone GRMC into experiments/grmc"
	@echo "  make update        pull latest GRMC"
	@echo "  make install-grmc  pip install -e GRMC"
	@echo "  make test-grmc     pytest GRMC"
	@echo "  make status        lab + grmc status"

setup:
	@bash "$(ROOT)scripts/setup_lab.sh"

update:
	@bash "$(ROOT)scripts/update_experiments.sh"

install-grmc: setup
	@cd "$(GRMC)" && pip install -e ".[dev]"

test-grmc: setup
	@cd "$(GRMC)" && pytest -q

status:
	@echo "=== Lab root ==="
	@echo "$(ROOT)"
	@echo ""
	@echo "=== Experiments ==="
	@ls -1 "$(ROOT)experiments" 2>/dev/null || true
	@echo ""
	@if [ -d "$(GRMC)/.git" ]; then \
		echo "=== GRMC git ==="; \
		git -C "$(GRMC)" log -1 --oneline; \
		echo ""; \
		echo "=== grmc status ==="; \
		mkdir -p "$(LAB_DATA)"; \
		cd "$(GRMC)" && grmc status --data-dir "$(LAB_DATA)" || \
		  echo "(install GRMC: make install-grmc)"; \
	else \
		echo "GRMC missing — run: make setup"; \
	fi
