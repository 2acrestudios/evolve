<h1>evolve</h1>
<img src="[https://2acrestudios.com/wp-content/uploads/2024/04/evolve.png" style="width: 300px;" align="right" />Like digital 'Sea Monkies' this Python script creates a simulation of evolving entities using Pygame and a local AI endpoint. Entities in this simulation exhibit basic behaviors such as movement and reproduction, with added complexities such as mutation, lifespan, and a reproductive cooldown period. The aim is to simulate an ecosystem where entities can mutate over generations, leading to a diverse range of attributes among the population. The AI endpoint is provided by running a local Ollama server using the Gemma:2b-instruct model.

<h3>Key Features:</h3>
<ol>
<li>Movement: Entities move randomly within the screen bounds.</li>
<li>Reproduction: Entities reproduce upon touching, subject to mutation rates and a reproduction limit to prevent overpopulation.</li>
<li>Mutation: Offspring can exhibit mutations, represented as changes in color and potentially other attributes such as size and speed.</li>
<li>Lifespan: Each entity has a finite lifespan, after which it is removed from the simulation, simulating a natural lifecycle.</li>
<li>Population Control: The simulation enforces a maximum population limit to maintain performance and ecosystem balance. A reproduction cooldown further prevents rapid population explosions.</li>
<li>AI Decisions: Entities fetch behavior decisions from a local AI model endpoint, allowing for dynamic interactions based on AI-generated instructions.</li>
</ol>

<h3>How It Works:</h3>
<ul>
<li>The simulation initializes a Pygame window with a predefined number of entities.</li>
<li>Each entity has properties such as position, size, color, speed, and lifespan.</li>
<li>A separate thread fetches decisions from a local AI model, directing entities to move or reproduce.</li>
<li>Entities reproduce by creating a new entity when they come into contact with another entity, with the offspring potentially exhibiting mutations.</li>
<li>The simulation keeps track of each entity's lifespan and reproduction cooldown, removing entities that have reached the end of their lifespan and limiting how frequently they can reproduce.</li>
<li>The script aims to showcase basic principles of artificial life simulations, including genetic variation, population dynamics, and lifecycle management, with a focus on creating a visually engaging and interactive simulation environment.</li>
<li>This project serves as a foundation for more complex simulations, offering insights into emergent behaviors and evolutionary principles in a controlled digital environment.</li>
</ul>
<h3>Requirements:</h3>
pygame==2.1.2<br />
requests==2.27.1<br />
ollama==0.1.31<br />
