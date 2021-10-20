# Introduction
This step-by-step tutorial can be completed in a pre-prepared environment that is contained in a Vagrant virtual machine. In order to start the virtual machine (VM), some dependencies must be installed:

#### Windows
- Vagrant
- VirtualBox

#### Mac
- Vagrant
- VirtualBox

#### Linux
- Vagrant
- VirtualBox OR libvirt

The VM is started with the following procedure:

1. On the command line, navigate to the folder that contains the file called `Vagrantfile`.
2. Run the command `vagrant up`.
3. Run the command `vagrant ssh`.

You should now be in the shell of the virtual machine.

# Installation

## Install *httk*

1. `git clone https://www.github.com/httk/httk.git`

2. The "devel" branch is the most up to date: `cd httk && git checkout devel`

3. Add `source ~/httk/init.shell` to your .bashrc file.
Doing so will make the `httk-*` command line scripts available in your terminal.
The `init.shell` will also add *httk*'s Python directory to your `$PYTHONPATH`, so it takes care of the Python installation.
    - Restart the terminal or run the command `source ~/.bashrc` to activate the changes.

> ### Note
> Alternative ways of installing httk:
> - Developer install:
>   - `cd ~/httk && pip install --editable . --user`
> - Normal install:
>   - `pip install httk`

# Initial httk setup
1. Run the command `httk-setup`.
2. Follow the instructions on screen.

A global configuration directory `.httk` will be created in your home folder.
The folder has the following structure:

```
.httk/
├── computers
├── config
├── keys
│   ├── key1.priv
│   └── key1.pub
└── tasks
```

- The **computers** folder contains global configuration of the supercomputers. Typically one configures computers within the *httk* project, so this folder can stay empty.
- The config file contains some global config information, such as user's name and email address.
- The **keys** folder contains to identify the "owner" of the data, e.g. when data is uploaded to a central database.
- The **tasks** folder remains empty most of the time.


# Setting up a new httk project
- `cd project`
- Run the command `httk-project-setup`.
- Follow the instruction on screen.

A new folder `ht.project` will be created in the `project` folder with the following structure:

```
ht.project/
├── config
├── keys
│   ├── key1.priv
│   ├── key1.pub
│   └── owner.pub
├── references
└── tags
```


# Setting up the computing clusters
1. In the project folder, run the command `httk-computer-setup`
2. When asked about setting up a project computer, answer yes.
3. The is asked to choose a template for the computer:
    - `local` is for testing, e.g. on your laptop.
    - `local-slurm` if your local machine has SLURM installed.
    - `ssh-slurm` is for the remote computing clusters.
4. We will setup a remote cluster, so choose `ssh-slurm`.
5. Follow the instructions on screen:
    - `Remote hostname`
      - Refers to the SSH hostname of the cluster, e.g. `tetralith.nsc.liu.se`
    - `Username`
      - Login username for the cluster, when you SSH into the cluster, e.g. `x_abcde`.
    - `Directory on remote host to keep runs and httk files: [Httk-runs]`
      - The path where to keep *httk*-related files, e.g. `/proj/theophys/users/x_abcde/Httk-runs`.
    - `The command to run vasp`
      - The command for executing VASP in the cluster, e.g. `mpprun /software/sse/manual/vasp/5.4.4.16052018/nsc1/vasp`.
    - `Vasp pseudopotential path`
      - The **absolute** path to the pseudopotential folder, e.g. `/software/sse/manual/vasp/POTCARs/potpaw_PBE.54`
    - `Slurm project`
      - The SLURM account whose CPU hours we want to consume, e.g. `snic2021-X-XXX`.

Once the computer setup is complete, a new folder called \<computer-name\> is created in `ht.project/computers`.
The configuration options that we specified above will be written to a file in `ht.project/computers/<computer-name>/config`.

> ### Note
> Currently *httk* does not have a sophisticated way to define how or how much computing resources should be allocated.
> In the config file one can change the `SLURM_NODES` parameter to correspond to the number of nodes we want the VASP calculations to parallelize over.

## Advanced computer setup
The basic config file can be extended by additional config files that must be named `config.<queue>`.
These additional config files contain options that either extend or override the basic options defined in `config`.
The `<queue>` extension in the `config.<queue>` file refers to a "queue" on the cluster.
The main purpose of queues is to keep tasks from different queues separate, so that the tasks can be managed separately.

- For example, if we want to be able to submit calculations using multiple SLURM accounts, we can create a config file called e.g. `config.snic2021-Y-YYY` that has the following content:
```
SLURM_PROJECT="snic2021-Y-YYY"
```

- As another example, often it is useful to be able to send quick test calculations to the testing/development reservation/partition of a cluster.
This can be done by creating a file called e.g. `config.devel` with appropriately defined parameters, for example:
```
SLURM_NODES="1"
SLURM_RESERVATION="devel"
SLURM_TIMEOUT="0-00:30:00"
```
The values of the parameters should be chosen in such a way that the calculation "fits" in the testing/development reservation/partition.

> ### Note
> In order to use the `SLURM_RESERVATION="devel"` option a modified version of *httk* is needed, because it is not (yet) implemented in the official *httk* git repository.


# Generating VASP input files
In a high-throughput scenario we want to generate the many input files in an automated way.
With *httk* one would typically write a Python script to do it.
In the `project` folder there is an example script that generates input files
for binary metal-nitrides in B1 structure.

- Run the command `python generate_Runs.py`

Once the script finishes running, a `Runs` folder has been created that contains the tasks, each in their own folder. The contents of the Runs folder should look like this:
```
Runs/
└── tetralith
    ├── ht.task.unassigned.AlN_B1.start.0.unclaimed.3.waitstart
    │   ├── ht_steps
    │   ├── INCAR.relax
    │   └── POSCAR
    └── ht.task.unassigned.TiN_B1.start.0.unclaimed.3.waitstart
        ├── ht_steps
        ├── INCAR.relax
        └── POSCAR
```

Tasks can be divided to be executed by multiple different queues, for example to balance the usage of CPU hours per project.
Here, all tasks are just under one queue, `tetralith`.

> ### Note
> *httk* has a standard way of naming these task folders `ht.task.XXX`.
> Information about the job and its status is encoded in the folder name using the "." character as a delimiter.

# Installing *httk* on the cluster
Before tasks can be executed on the cluster, we have to install *httk* there.
- In the project folder, run the command `httk-computer-install <computer-name>`.

# Sending tasks to the cluster
Tasks are sent to the cluster with the command:
- `httk-tasks-send-to-computer <computer-name>:<queue> <runs-folder>`

> ### Note
> If we want to use the "default" queue, then we can omit the `:<queue>` part in the command and just run
> - `httk-tasks-send-to-computer <computer-name> <runs-folder>`

In our case we will use the Tetralith cluster and the default queue, so the command looks like:
- `httk-tasks-send-to-computer tetralith Runs/tetralith`.

> ### Note
> The `<queue>` parameter will determine where in the cluster the tasks are placed.
> The location has the form
> - `${REMOTE_HTTK_DIR}/Runs/<queue>`,
>
> where the `${REMOTE_HTTK_DIR}` variable is defined in the computer's config file.

# Start the taskmanager
The taskmanager that manages and runs the tasks on the cluster is started with the command:
- `httk-tasks-start-taskmanager <computer-name>:<queue> NUMBER`

The `NUMBER` argument refers to the number of taskmanagers that will be spawned and run concurrently. Each taskmanager allocates the number of nodes that is defined in the `<computer-name>`'s config file with the `SLURM_NODES` parameter.

> ### Note
> The `NUMBER` argument is optional, and if it is omitted, only one taskmanager will be spawned.

# Receiving calculations from the cluster
Once the calculations have finished, one can download the output files from the cluster with the following command:
- `httk-tasks-receive-from-computer <computer-name>:<queue>`

# Storing results in a (local) database
VASP output files are analyzed and data stored in an SQLite database by *httk*.
The project folder contains an example Python script `make_database.py` that accomplishes this.
- Run the script: `python make_database.py`

An SQLite file called `example.sqlite` will be produced.

One can verify that a functional database was created by running the example `read_database.py` Python script.
The printout should look something like this:
```
Formula: AlN       , total_energy =  -14.530
Formula: NTi       , total_energy =  -19.572
```


# Advanced topics
- Using a Python runscript instead of the bash version.
















