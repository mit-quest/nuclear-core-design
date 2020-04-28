This repository is under development. Expect anything in it to change rapidly.

# nuclear-core-design
## Install Procedure
1. Clone the repository and `cd` into it 
2. Run `make`

You have now successfully installed the repository!

## Setup of Keys

You will need two keys associated with the gcp project, "bridge-urops". The first is a service account, follow the [instructions](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and put the resulting json in the keys directory.
The second is a key to the cloud storage, follow the [instructions](https://github.com/s3fs-fuse/s3fs-fuse/wiki/Google-Cloud-Storage#get-credentials) and put the resulting gcs-auth.txt file in the keys directory.

## Running the test example:
1. Run `source .venv/bin/activate` to enter the virtual environment
2. Run `python test_tune.py` to see Rllib train a PPO agent on CartPole and perform a grid search for the best learning rate

## Training an Agent
There is one script that can train an agent on any of the the environments. Simply run the script and specify a config file, `python any_tune.py -c path-to-config`, for example `python any_tune.py -c configs/float_default_config.yaml`. 
By default, if no `-c` flag is specified, the default config file is `config/swap_default_config.yaml`. For details on config parameters specific to each environment see the section below. To pass arguments to tune.run() put them in the
tune section of the config. Note that the algorithm must be specified in its own entry per the example configs. Additionally, any arguments that include python code and must be evaluated before being passed to tune.run() should go in the
to_eval section of the config as shown by the examples. If you run into any errors with your config file, you can run the `any_tune.py` script with the `-d` flag which will turn on a debug print that shows you exactly how your paramaters
are being passed to tune.run().

## Environments
### Coloring Environment

The purpose of the Coloring Environment is to serve as an optimization test over a parameterized number of discrete variables. See a detailed description of the environment and how to create a configuration file to run agents in it [here](colorenv/README.md).

### Float Environment

The purpose of the Float Environment is to serve as an optimization test over a parameterized number of continuous variables. See a detailed description of the environment and how to create a configuration file to run agents in it [here](floatenv/README.md).

### Swap Environment

The purpose of the Swap Environment is to serve as an optimization test over a parameterized number of discrete variables. See a detailed description of the environment and how to create a configuration file to run agents in it [here](swapenv/README.md).

### BWR6x6 Environment

The purpose of the BWR6x6 Environment is to serve as an optimization test for a true nuclear core design problem. See a detailed description of the environment and how to create a configuration file to run agents in it [here](bwr6x6env/README.md).

## Visualization:
After running one of the tune script you can run `tensorboard --logdir=results` in another window to visualize training in your browser.

## Distributed Training:
### Setup
1. `terraform apply`
2. `make clusterConnect`
3. `ray up kubernetes-full.yaml`

### Run
1. `ray attach kubernetes-full.yaml`
2. `python3 cluster_tune -c path/to/config.yaml`

### Teardown
1. `ray down kubernetes-full.yaml`
2. `terraform destroy`
