.PHONY: build verify verify-site verify-math
build:
	python3 tools/build_site.py
verify: verify-site verify-math
verify-site:
	python3 -m unittest discover -s tools -p 'test_*.py'
	python3 tools/check_site.py
verify-math:
	$(MAKE) -C oeis verify
	$(MAKE) -C bb6 verify
	$(MAKE) -C horizonmath verify
