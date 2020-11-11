# USC-CARC-test_paranrn

This code is specific for testing your parallel PyNEURON installation on the CARC Discover cluster. 

Using this code to run a parallel network on your own computer will be slightly different.

Information on the commands to format and submit jobs in the Discover cluster were taken from this website: https://carc.usc.edu/user-information/user-guides/high-performance-computing/discovery

## Installing nrn-7.8 (or latest stable version)
To install the latest stable version of NEURON, use the following command:

```
$ pip3 install --user neuron
```

## Installing nrn-7.7

A bash wrapper and the source files for installing nrn-7.7 are provided.

**Before you run the script, you must first open the file and change PWD to match the directory in which you want to install NEURON.**

Run the install_nrn script using the following command:

```
$ ./install_nrn.sh
```

If install_nrn is not executable, then you will need to run the following:

```
$ chmod u+x install_nrn.sh
```

## Submitting a job
The guide to submitting a job can be found here: https://carc.usc.edu/user-information/user-guides/high-performance-computing/discovery/running-jobs

Before submitting a job, **you must first edit the following lines in each Slurm script to point to your installation of NEURON.**

### For nrn-7.8
* The NEURON_PATH variable and the ```export PYTHONPATH...``` commands are unnecessary and can be deleted.

### For nrn-7.7
* Default line
```
NEURON_PATH=/project/berger_92/geneyu/Big_Model/USC-CARC-test_paranrn/nrn-7.7
```

* Change default line to...
```
NEURON_PATH=PATH_TO_YOUR_NEURON_INSTALLATION
```

### Account name
The account name will have to be changed if it is not berger_92. See the following line:
```
#SBATCH ---account=berger_92
```
Enter the command ```myaccount``` to see your available accounts.

### Example command for submitting a job (any nrn version)
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

## Tutorial for specifying a parallel network
The following guide can be used to understand the syntax for creating a network with neurons distributed across different processes:

https://www.neuron.yale.edu/neuron/docs/ball-and-stick-model-part-4

This guide also uses code from the previous part: https://www.neuron.yale.edu/neuron/docs/ball-and-stick-model-part-3

## test_parallel_network.py
This script creates models that are distributed across different processes and need to communicate with neurons on different processes. A network is constructed that requires communication between spike generators and neurons that exist on different processes. It requires the ParallelContext object from NEURON to be instantiated to handle the parallel network communication.

## test_distirbute_neurons.py
This script is an example for distributing neurons across different processes but only need to communicate with neurons on the same process. This may be useful for investigating the effects of different parameters on the same neuron model. It uses mpi4py to handle the parallel distribution of these neurons across different processes.
