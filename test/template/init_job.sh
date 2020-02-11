#!/bin/sh
#SBATCH -J init_scaling_test
#SBATCH -p skx-normal
#SBATCH -t 48:00:00
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=24
#SBATCH -A TG-AST120025
#SBATCH --mail-user=cchoban@ucsd.edu
#SBATCH --mail-type=all
#SBATCH -o job.log
#SBATCH --export=ALL
#SBATCH -D .
set -e
pwd
date
source ./activate.sh
export OMP_NUM_THREADS=2

MPIRUN="ibrun"

if [[ -d output/restartfiles ]]; then
    # Restart
    $MPIRUN tacc_affinity ./GIZMO init_parameters.txt 1
else
    # Start from scratch
    $MPIRUN tacc_affinity ./GIZMO init_gizmo_parameters.txt
fi
