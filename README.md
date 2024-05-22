<h1>evolve</h1>
<img src="https://2acrestudios.com/wp-content/uploads/2024/04/evolve.png" style="width: 300px;" align="right" />Like digital 'Sea Monkies' this Python script creates a simulation of evolving entities using Pygame and a local AI endpoint. Entities in this simulation exhibit basic behaviors such as movement and reproduction, with added complexities such as mutation, lifespan, and a reproductive cooldown period. The aim is to simulate an ecosystem where entities can mutate over generations, leading to a diverse range of attributes among the population. The AI endpoint is provided by running a local Ollama server using the Gemma:2b-instruct model.
To create a complete README file for the provided script, I'll first analyze the script to understand its functionality and structure. Then, I'll generate a comprehensive README.md file.

## Features

- **Graphical Simulation**: Uses Pygame to create a visual representation of the evolutionary process.
- **Organism Behavior**: Organisms can move, eat, reproduce, and die based on defined rules and energy constraints.
- **Configurable Parameters**: Adjust population limits, lifespan, food count, energy consumption, and other parameters to observe different evolutionary outcomes.

## Requirements

- Python 3.x
- Pygame
- Requests

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/evolution-simulation.git
    cd evolution-simulation
    ```

2. Install the required dependencies:
    ```bash
    pip install pygame requests
    ```

## Usage

Run the simulation using the following command:
```bash
python evolve-v2.py
```

## Parameters

You can modify the parameters in the script to observe different behaviors and outcomes in the simulation:

- `POPULATION_LIMIT`: Maximum number of organisms.
- `SIZE_LIMIT`: Maximum size of organisms.
- `LIFESPAN_LIMIT`: Maximum lifespan of organisms in cycles.
- `FOOD_COUNT`: Number of food sources available.
- `REPRODUCTION_FOOD_THRESHOLD`: Minimum food required for an organism to reproduce.
- `REPRODUCTION_BONUS`: Size increase after reproduction.
- `INITIAL_ENERGY`: Initial energy for organisms.
- `ENERGY_GAIN`: Energy gained from eating food.
- `ENERGY_COST`: Energy cost per move.

## Example

```python
# Modify these values in evolve-v2.py to see different results
POPULATION_LIMIT = 100
SIZE_LIMIT = 20
LIFESPAN_LIMIT = 300
FOOD_COUNT = 480
REPRODUCTION_FOOD_THRESHOLD = 3
REPRODUCTION_BONUS = 1
INITIAL_ENERGY = 10
ENERGY_GAIN = 2
ENERGY_COST = 0.1
```

<img src="https://2acrestudios.com/wp-content/uploads/2024/05/Screenshot-2024-05-22-at-9.52.53 AM-12.png" />
