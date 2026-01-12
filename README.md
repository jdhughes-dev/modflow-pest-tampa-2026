# 2026 Florida MODFLOW 6 & PEST++ Training

![https://en.wikipedia.org/wiki/File:Tampa_Florida_November_2013-2b.jpg](images/image-1.png)

## Class materials for 2026 MODFLOW / PEST class in Tampa, Florida 

Tuesday January 20, 2026 8:00 AM - Friday January 23, 2026 2:00 PM

## Install instructions

0) install mini-forge.  See instructions here: [https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge)
1) clone/download this repo and open a terminal/cmd window in that dir (you might have to use the Miniforge Prompt on windows)
2) create the `tampa26mf6pp` environment: `mamba env create -f environment.yml`
3) activate the environment: `mamba activate tampa26mf6pp`
4) install modflow6: `get-modflow --repo modflow6-nightly-build :python`
5) install pest++: `get-pestpp --release-id 5.2.25 :python`
6) check that mf6 and pestpp-ies are working by calling the following executables
  - `mf6`
  - `pestpp-ies`
  - `pestpp-opt`
7) check that the jupyter notebook is working properly by calling `jupyter notebook`

If you made it this far...#winning


### <u>Tentative training agenda</u>:

#### __Tuesday - MODFLOW 6__
| Start Time | End Time  | Type | Topic |
| ---------- | -------- | ---- | ----- |
| 8:00 AM | 9:00 AM | **Presentation** | MODFLOW 6 Overview
| 9:00 AM | 9:30 AM | **Software installation** | testing and troubleshooting
| 9:30 AM| 11:00 AM | **Presentation<br>Hands-on** | getting started with MODFLOW 6 and unstructured grids
| 11:00 AM | 12:00 PM | **Presentation<br>Hands-on** | UZF package
| 1:00 PM | 1:30 PM | **Presentation<br>Hands-on** | MAW package
| 1:30 PM | 3:00 PM | **Presentation<br>Hands-on** | SFR, LAK, and MVR packages
| 3:00 PM | 4:00 PM | **Presentation<br>Hands-on** | Particle tracking with the PRT model

#### __Wednesday - MODFLOW 6__
| Start Time | End Time  | Type | Topic |
| ---------- | -------- | ---- | ----- |
| 8:00 AM | 8:30 AM | **Presentation<br>Hands-on** | variable density concepts and simulations 
| 8:30 AM | 9:00 AM | **Hands-on** | variable density concepts and simulations 
| 9:00 AM | 10:00 AM | **Presentation<br>Hands-on** | parallel model simulations 
| 10:00 AM | 11:00 AM | **Presentation<br>Hands-on** | deep dive on solver settings
| 11:00 AM | 12:00 PM | **Presentation<br>Hands-on** | MODFLOW 6 Application Programming Interface (API)
| 1:00 PM | 2:00 PM | **Presentation<br>Hands-on** | MODFLOW 6 Adjoint (MF6-ADJ) and current/future MODFLOW 6 developments

#### __Thursday - PEST++__
| Start Time | End Time  | Type | Topic |
| ---------- | -------- | ---- | ----- |
|  8:00 AM | 9:00 AM | **Presentation** | calibration, parameters, predictions, and data
| 9:00 AM | 11:00 AM | **Hands-on** | setting up a pest interface manually. understanding parallelization concepts
| 11:00 AM | 12:00 PM | **Presentation** | pilot points, geostatistics, and heterogeneity
| 1:00 PM | 2:30 PM | **Hands-on** | automating pest interface construction, setting obs vals and weights
| 2:30 PM | 3:30 PM | **Presentation**  | ensemble methods
| 3:30 PM | 4:30 PM | **Hands-on** | initial ies run

#### __Friday - PEST++__
| Start Time | End Time  | Type | Topic |
| ---------- | -------- | ---- | ----- |
| 9:00 AM | 10:00 AM | **Hands-on** | running experiments with ies to understand how the prior, weights, and noise influence results
| 10:00 AM | 11:00 AM | **Presentation** | management optimization
| 11:00 AM | 12:00 PM | **Hands-on** | running experiments with opt to understand how bounds and constraints influence results
| 1:00 PM | 2:00 PM | **Discussion** | bring your questions!

## Software

We will be using Jupyter notebooks during the class.  Software installation instructions for the class are included [here](./software.md).