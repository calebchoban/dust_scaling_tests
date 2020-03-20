#!/bin/sh
#SBATCH -J restart_job
#SBATCH -p skx-normal
#SBATCH -t 1:00:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=24
#SBATCH -A TG-AST120025
#SBATCH --mail-user=cchoban@ucsd.edu
#SBATCH --mail-type=all
#SBATCH -o test.log
#SBATCH --export=ALL
#SBATCH -D .
set -e
pwd
date
source ../../../../activate.sh
export OMP_NUM_THREADS=2
MPIRUN="ibrun"
SECONDS=0
date
$MPIRUN tacc_affinity ./GIZMO gizmo_parameters.txt 2
date
echo "Code finished in $(($SECONDS/60)) min $(($SECONDS%60)) sec" 
echo $SECONDS
