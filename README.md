# evolve
This Python script creates an interactive simulation of evolving entities using Pygame. Entities in this simulation exhibit basic behaviors such as movement and reproduction, with added complexities such as mutation, lifespan, and a reproductive cooldown period. The aim is to simulate an ecosystem where entities can mutate over generations, leading to a diverse range of attributes among the population.

Key Features:
1. Movement: Entities move randomly within the screen bounds.
2. Reproduction: Entities reproduce upon touching, subject to mutation rates and a reproduction limit to prevent overpopulation.
3. Mutation: Offspring can exhibit mutations, represented as changes in color and potentially other attributes such as size and speed.
4. Lifespan: Each entity has a finite lifespan, after which it is removed from the simulation, simulating a natural lifecycle.
5. Population Control: The simulation enforces a maximum population limit to maintain performance and ecosystem balance. A reproduction cooldown further prevents rapid population explosions.
6. AI Decisions: Entities fetch behavior decisions from a local AI model endpoint, allowing for dynamic interactions based on AI-generated instructions.

How It Works:
- The simulation initializes a Pygame window with a predefined number of entities.
- Each entity has properties such as position, size, color, speed, and lifespan.
- A separate thread fetches decisions from a local AI model, directing entities to move or reproduce.
- Entities reproduce by creating a new entity when they come into contact with another entity, with the offspring potentially exhibiting mutations.
- The simulation keeps track of each entity's lifespan and reproduction cooldown, removing entities that have reached the end of their lifespan and limiting how frequently they can reproduce.
- The script aims to showcase basic principles of artificial life simulations, including genetic variation, population dynamics, and lifecycle management, with a focus on creating a visually engaging and interactive simulation environment.
- This project serves as a foundation for more complex simulations, offering insights into emergent behaviors and evolutionary principles in a controlled digital environment.
