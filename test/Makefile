GIZMO_GIT_SRC ?= https://calebchoban@bitbucket.org/calebchoban/gizmo.git
BRANCH_NAME ?= dust_routines


# default command
# prints out the MakeFile to see what it does
.PHONY: help
help:
	cat Makefile

# Download GIZMO and all other necessary files
.PHONY: clone
clone:
	git clone --single-branch --branch $(BRANCH_NAME) $(GIZMO_GIT_SRC)
	curl http://www.tapir.caltech.edu/~phopkins/public/spcool_tables.tgz | tar xz
	ln -s gizmo/cooling/TREECOOL TREECOOL

# Compile and run initial sims
.PHONY: init
init:
	mkdir runs
	python init_runs.py

# Compiles GIZMO with and without dust
.PHONY: compile
compile: GIZMO

GIZMO: Makefile.systype Config.sh
	cp Makefile.systype gizmo/
	cp Config.sh gizmo/
	source ./activate.sh && cd gizmo && make
	mv gizmo/GIZMO ./GIZMO

.PHONY: tests
tests:
	python scaling_tests.py

# cleans up the current and gizmo directory
.PHONY: clear
clear:
	rm -rf runs/ gizmo/ TREECOOL spcool_tables/
