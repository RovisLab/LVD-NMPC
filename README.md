# DL-B-NMPC: Deep Learning-based Behavioral Nonlinear Model Predictive Control for Autonomous Vehicles

This repository accompanies the *DL-B-NMPC: Deep Learning-based Behavioral Nonlinear Model Predictive Control for Autonomous Vehicles* paper.

DL-B-NMPC uses an *a-priori* process model in combination with behavioral and disturbance models. The models are responsible for estimating the controlled system's desired state trajectory for different operating conditions, acting as input to a constrained NMPC. We propose to encode both models within the layers of a deep neural network, which acts as a nonlinear approximator for the high order state-space of the operating conditions. The input is based on historical sequences of system states and observations, integrated by an Augmented Memory component. We use Inverse Reinforcement Learning and the Bellman optimality principle to train our learning controller with a modified version of the Deep Q-Learning algorithm, enabling us to estimate the desired state trajectory as an optimal action-value function. We evaluate DL-B-NMPC against the baseline Dynamic Window Approach (DWA), End2End and Reinforcement learning methods for vehicle control. Performance is measured in our simulation environment GridSim, on a real-world 1:8 scaled model car, as well as on a real size autonomous test vehicle.

![Alt text](images/dl_b_nmpc_block_diagram.png?raw=true)

## Installation

## Run pre-trained models