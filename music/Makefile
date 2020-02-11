HPC ?= tscc

.PHONY: compile
compile:
	cd compile && HPC=$(HPC) make


.PHONY: run
run:
    ifeq ($(HPC),tscc)
	    cd run && qsub job.pbs
    else
	    cd run && sbatch job.sh
    endif
