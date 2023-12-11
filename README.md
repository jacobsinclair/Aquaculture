# Aquaculture Simulation :fish: :seedling:

This is a Continuous-Time Simulation of the fluctuation of chemicals in an Aquarium system. The chemicals we are keeping track of in the state of our aquarium are: Ammonium, Nitrite, Nitrate, Nitrogen gas, Disolved Oxygen and pH. Our goal is to predict if an aquarium configuration (Size, Temp, Lighting, Fish, Plants) will be self sufficent, require water changes / feeding or will not support life. 

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started
To use the simulation, download both aquarium.py and fish.py.
The file aquarium.py is our driver class, carrying out the work of the simulation, 
while fish.py is the object class which determines the attributes and behaviors of the fish
in our simulation. **YOU MUST HAVE THE FILES IN THE SAME DIRECTORY FOR IT TO RUN**

* Simply run the aquarium.py file through your console/terminal or IDE
  and input your desired parameters. (type python aquarium.py if using console or terminal)
* The file will run the simulation and give you the amount of time it will take to complete.
* You will then be given output in the form of graphs which can be saved to a file if you wish.

## Prerequisites

Python

Python libraries:
* numpy
* matplotlib
* alive_progress
* PyQt5

## Installation

Install Python here:
* https://www.python.org/downloads/

To install needed packages we recommend downloading the pip installer, 
you can follow this tutorial to do so:
* https://www.geeksforgeeks.org/how-to-install-pip-on-windows/

When you have installed python and pip, you can then install the python libraries. 
To do so simply go to your console/terminal and enter: pip install packageName

## Usage

[Provide examples and explanations of how to use the project.]

## Contributing

[Explain how others can contribute to the project. Include guidelines for pull requests and code of conduct if applicable.]

## License 

[Include the type of license the project is under. For example, MIT License, Apache License 2.0, etc.]
