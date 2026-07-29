PYTHON ?= python3
export PYTHONPATH := $(CURDIR)/src

.PHONY: preflight build-dataset test evaluate analyze reproduce verify release-bundle clean

preflight:
	$(PYTHON) scripts/environment_preflight.py

build-dataset:
	$(PYTHON) scripts/build_dataset.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

evaluate:
	$(PYTHON) scripts/run_evaluation.py --run-id pilot-primary

analyze:
	$(PYTHON) scripts/analyze_results.py --input results/raw/pilot-primary.jsonl

reproduce:
	$(PYTHON) scripts/verify_reproducibility.py

verify: preflight build-dataset test evaluate analyze reproduce

release-bundle:
	$(PYTHON) scripts/build_release.py

clean:
	rm -rf results/raw/* results/tables/* results/figures/* results/reports/* artifacts/* logs/*.log
