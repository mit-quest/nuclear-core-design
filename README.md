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

### Casmo10x10 Environment

The purpose of the Casmo10x10 Environment is to serve as an optimization test for a large scale nuclear core design problem. There are no specific gym paramaters to control. 

## Visualization:
After running one of the tune script you can run `tensorboard --logdir=results` in another window to visualize training in your browser.

## Training On Cloud Machines
Note that this requires you to complete the setup keys section above. The number of machines and their specifications are controlled by the terraform.tfvars file.
1. Run `terraform apply` this will create the machines (you'll generally want to `make clean` before this or it will take forever to copy the repository over)
2. Connect with `ssh -i private_ssh_key_location username@server_ip` where private_key_location and username match the variables specified in the terraform.tfvars file. You can find the server ip in the gcp compute console.
3. Run `cd nuclear-core-design/; source .venv/bin/activate; make mount` 
4. Run `python3 any_tune.py -c path/to/config.yaml`

### Visualizing On Cloud Machines
1. `ssh -L 16006:127.0.0.1:6006 -i private_ssh_key_location username@server_ip` will open an ssh window that forwards port 6006 on the server to localhost:16006
2. Run `cd nuclear-core-design/; source .venv/bin/activate` 
3. Run `tensorboard --logdir=results`
4. Navigate to `localhost:16006` in your browser
