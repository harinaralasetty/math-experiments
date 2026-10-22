CXX = clang++
CXXFLAGS = -O3 -std=c++17 -Wall -Wextra
PROGRAMS = code/new_powerful code/new_patterns code/cut_runs code/new_runs code/stage4/necklaces code/stage4/independent
.PHONY: verify quick
verify: $(PROGRAMS)
	python3 -u verify.py
quick: $(PROGRAMS)
	python3 -u verify.py --quick
code/%: code/%.cpp
	$(CXX) $(CXXFLAGS) $< -o $@
