# USC-CARC-test_paranrn

This code is specific for testing your parallel PyNEURON installation on the CARC Discover cluster. 

Using this code to run a parallel network on your own computer will be slightly different.

Information on the commands to format and submit jobs in the Discover cluster were taken from this website: https://carc.usc.edu/user-information/user-guides/high-performance-computing/discovery

## Installing PyNEURON for nrn-7.7

A bash wrapper for installing PyNEURON is provided and named install_nrn.

**Before you run the script, you must first open the file and change PWD to match the directory in which you want to install NEURON.**

Run the install_nrn script using the following command:

```
$ ./install_nrn.sh
```

If install_nrn is not executable, then you will need to run the following:

```
$ chmod u+x install_nrn.sh
```

With nrn-7.7, you will not need to run the install_pyneurons.sh script.

## Submitting a job
The guide to submitting a job can be found here: https://carc.usc.edu/user-information/user-guides/high-performance-computing/discovery/running-jobs

For the example scripts, **you must first edit the following lines in each Slurm script to point to your installation of NEURON.**

Default line
```
NEURON_PATH=/project/berger_92/geneyu/Big_Model/USC-CARC-test_paranrn/nrn-7.7
```

New line
```
NEURON_PATH=PATH_TO_YOUR_NEURON_INSTALLATION
```

Also, the account name will have to be changed if it is not berger_92. See the following line:
```
#SBATCH ---account=berger_92
```
Enter the command ```myaccount``` to see your available accounts.

### Example command for submitting a job
```
$ sbatch slurm_parallel_network.slurm
```

## Understanding the Slurm script
The guide for setting up a Slurm script is here: https://carc.usc.edu/user-information/user-guides/high-performance-computing/discovery/getting-started

The guide for setting up an MPI-Only Slurm script is here: https://carc.usc.edu/user-information/user-guides/high-performance-computing/discovery/slurm-templates

Note that the number of tasks in #SBATCH --ntasks and mpirun command lines need to match.

Ex:

```#SBATCH --ntasks=```**4**

```mpirun -bind-to core -np``` **4** ```python test_distribute_neurons.py```

## Interactive mode
See: https://carc.usc.edu/user-information/user-guides/high-performance-computing/discovery/getting-started (Testing your job section)
"Interactive jobs are similar to batch jobs but **all actions are typed manually on the command line**, rather than in a script. The main advantage of an interactive job is that you get immediate feedback and the job will not end (and put your compute resources back into the pool) if your program errors out. This makes interactive jobs ideal test environments for people who aren't sure what to put in their job scripts."

An interactive session can be started usig the following command:
```
salloc --ntasks=4 --time=1:00:00 --account=<account_id>
```

In the interactive session, you should have your slurm script opened in another window to copy and paste the commands for debugging. You do not need to copy and paste the ```#SBATCH``` lines. Only enter the lines beginning with the module load and onward.

