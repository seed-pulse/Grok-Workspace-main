.PHONY: help setup update status test-grmc install-grmc doctor seed-grmc memory-sync

ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
GRMC := $(ROOT)experiments/grmc
LAB_DATA := $(ROOT).lab_data/grmc
LABCTL := python3 "$(ROOT)tools/labctl.py"

help:
	@echo "Grok-Workspace-main"
	@echo "  make setup          clone/init GRMC submodule"
	@echo "  make update         pull latest GRMC"
	@echo "  make install-grmc   pip install -e GRMC"
	@echo "  make test-grmc      pytest GRMC"
	@echo "  make doctor         lab sanity checks"
	@echo "  make status         labctl status (+ grmc)"
	@echo "  make seed-grmc      ingest seeds+inbox+self_model into GRMC"
	@echo "  make memory-sync    seed-grmc then reflect (no graph write)"

setup:
	@bash "$(ROOT)scripts/setup_lab.sh"

update:
	@bash "$(ROOT)scripts/update_experiments.sh"

install-grmc: setup
	@cd "$(GRMC)" && pip install -e ".[dev]"

test-grmc: setup
	@cd "$(GRMC)" && pytest -q

doctor:
	@$(LABCTL) doctor

status:
	@$(LABCTL) status

seed-grmc: setup
	@mkdir -p "$(LAB_DATA)"
	@$(LABCTL) seed-grmc --all

memory-sync: setup
	@mkdir -p "$(LAB_DATA)"
	@$(LABCTL) seed-grmc --all --reflect
