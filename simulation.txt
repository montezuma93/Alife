#!/bin/bash
#SBATCH -p test_cpu-ivy
#SBATCH --mem=2G
#SBATCH --time=8:00:00
python3 ./SimulationScript.py