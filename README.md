# Taking Care of Beezness - COMP5005 Postgraduate Assignment

## Overview

This project is a simulation of a honey bee colony and its interactions within a 2D property environment. The simulation models bee behaviour, nectar collection, hive management, communication strategies, and environmental obstacles.

Developed as part of **COMP5005 – Fundamentals of Programming**, Curtin University, Semester 1, 2025.

## Objectives

The simulation aims to:

* Model bee movement between the hive and the environment.
* Simulate nectar collection and honey production.
* Represent flowers, trees, buildings, water, and other terrain features.
* Compare random and directed foraging strategies.
* Evaluate the impact of bee communication on hive efficiency.
* Support both interactive and batch execution modes.

## Features

### Bees

* Worker bee objects with position and state tracking.
* Mission-based nectar collection.
* Hive-to-world and world-to-hive navigation.
* Communication of nectar source locations.

### Environment

* 2D map-based world.
* Flowers and trees as nectar sources.
* Buildings and water as barriers.
* Configurable terrain loaded from CSV files.

### Simulation

* Time-step driven behaviour.
* Automated bee actions and interactions.
* Honey accumulation tracking.
* Parameter-driven experimentation.

## Running the Simulation

### Interactive Mode

```bash
python beeworld.py -i
```

### Batch Mode

```bash
python beeworld.py -f map1.csv -p params1.csv
```

## Example Parameters

Parameters may include:

* Number of bees
* Hive size
* Simulation duration
* Communication probability
* Nectar collection capacity
* Mission strategy type

## Research Focus

This postgraduate project investigates:

1. Random versus directed nectar-search strategies.
2. The impact of communication between bees.
3. Hive efficiency under varying environmental conditions.

## Technologies

* Python 3
* Object-Oriented Programming
* CSV-based configuration files

## Contents

* README.md - readme file for Assignment

* models/bee.py - Implementation of bees' behaviors, state etc.

* models/environment.py - Arranging the hive, flowers, obstacles, and bees in beeworld

* models/flower.py - Implementation of flower program

* models/hive.py - Implementation of hive program for data count

* models/terrain.py - Implementation of obstacles

* utils/config_loader.py - A program for loading the csv files

* utils/settings.py - Simulation configuration

* vutils/visuals.py - All the works related to visualizations

* beeworld.py - Main simulation program for this assignment

* `__init__.py` - unused files

* `__pycache__` - auto generated folder

* map1.csv - A CSV file for terrain program (Batch mode only)

* params1.csv - A CSV file for parameter setups (Batch mode only) 

* Project_Report - A report related to the assignment

* 2025 Sem 1 COMP5005 Assignment - v1.0 - Instructions for the assignment


## Dependencies

* numpy

* random

* time

* matplotlib.pyplot

* argparse

* matplotlib.colors

* matplotlib.patches 


## Version Information

05/05/2025 - Initial version of Assignment programs

17/05/2025 - Final version of Assignment programs


## Author

Abu Fatah Mohammed Faisal

Curtin University

Master of Predictive Analytics

## License

This repository is submitted as coursework for COMP5005 and is intended for academic use only.
