# LVD-NMPC: Learning-based Vision Dynamics Nonlinear Model Predictive Control for Autonomous Vehicles

This repository accompanies the *LVD-NMPC: A Learning-based Vision Dynamics Approach to Nonlinear Model Predictive Control for Autonomous Vehicles* paper.

LVD-NMPC uses a vision dynamics model in combination with an a-priori process model. The vision dynamics model is used to estimate the dynamics of the driving scene, the controlled system's desired state trajectory and the weighting gains of the quadratic cost function optimized by a constrained NMPC. We propose to encode the vision model within the layers of a deep neural network, which acts as a nonlinear approximator for the high order state-space of the operating conditions. The input is based on historic sequences of system states and observations, integrated by an Augmented Memory component. We train our learning controller with a modified version of the Deep Q-Learning algorithm, enabling us to estimate the visual dynamics as an optimal action-value function of the desired state trajectory. We evaluate LVD-NMPC against a baseline Dynamic Window Approach (DWA) path planning executed using standard NMPC, as well as against the PilotNet neural network. Performance is measured in our simulation environment GridSim, on a real-world 1:8 scaled model car, as well as on a real size autonomous test vehicle.

![Alt text](images/lvd_nmpc_block_diagram.png?raw=true)

## Installation

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Clone the repository:
```bash
$ git clone https://github.com/RovisLab/LVD-NMPC.git
```

The packages needed for install can be found inside requirements.txt: 

```
pip install -r requirements.txt
```

### Running the code

Each of the algorithms has a main function inside its own script, where a few parameters can be modified in order to run it. 
They all run inside GridSim, which is an autonomous driving simulator engine that uses a car-like robot architecture to generate occupancy grids from simulated sensors.

#### Neuro-evolution

The script is: 
```
car_kinematic_ga.py
```

There is a boolean parameter, called *train_ga*, which enables the prediction and the training of the neuro-evolutionary algorithm.
If *train_ga* is set to **False**, a pre-defined elite model will be loaded, and will run into the seamless scenario inside GridSim.
If *train_ga* is set to **True**, the agent will start training, based on the parameters *nr_population* and *nr_generations*.

#### Dynamic Window Approach

The script is: 
```
car_kinematic_replay_dwa.py
```

This script will run the dynamic window approach, which performs the local path planning given the obstacles from the sensor. It will run in the Stockholm city scenario.
The parameters which can be modified are inside *dynamic_window_approach.py*. 

#### Deep Q Network

The script is: 
```
car_kinematic_dqn.py
```

This script will run the DQN agent inside the city scenario, and it will print out the episode together with the associated reward, as the agent learns to navigate the environment.

#### Model Predictive Control

The script is: 
```
car_kinematic_mpc.py
```

The script will run the MPC controller on a reference trajectory found in the resources/mpc_ref.csv file. It will run in the Stockholm city scenario.

## Built with

* [Pygame](https://www.pygame.org/news) - A python programming language library for making multimedia applications like games built on top of the SDL library.
* [Tensorflow](https://www.tensorflow.org/) - An open source machine learning framework for everyone.
* [Numpy](http://www.numpy.org/) - NumPy is the fundamental package for scientific computing with Python.


