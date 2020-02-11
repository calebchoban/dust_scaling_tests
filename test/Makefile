GIZMO_GIT_SRC ?= https://calebchoban@bitbucket.org/calebchoban/gizmo.git
BRANCH_NAME ?= dust_routines


# default command
# prints out the MakeFile to see what it does
.PHONY: help
help:
	cat Makefile

# Download GIZMO and all other necessary files
.PHONY: init
init:
	git clone --single-branch --branch $(BRANCH_NAME) $(GIZMO_GIT_SRC)
	curl http://www.tapir.caltech.edu/~phopkins/public/spcool_tables.tgz | tar xz
	ln -s gizmo/cooling/TREECOOL TREECOOL
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

# submits a job to the queue
.PHONY: submit
submit:
	sbatch job.sh

# cleans up the current and gizmo directory
.PHONY: clear
clear:
	rm -rf runs/ gizmo/ TREECOOL spcool_tables/
