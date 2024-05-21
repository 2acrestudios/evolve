import pygame
import requests
import json
import random
import time
import math
import threading
from queue import Queue

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolution Simulation")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 105, 180)
RED = (255, 0, 0)

# Ollama local API endpoint
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

# Population limits
POPULATION_LIMIT = 100
SIZE_LIMIT = 10
LIFESPAN_LIMIT = 500  # Number of cycles an organism can live
FOOD_COUNT = 480  # Number of food sources
REPRODUCTION_FOOD_THRESHOLD = 3  # Minimum food needed to reproduce
REPRODUCTION_BONUS = 3  # Bonus size increase after reproduction
INITIAL_ENERGY = 100  # Initial energy for organisms
ENERGY_GAIN = 10  # Energy gained from eating food
ENERGY_COST = 0.2  # Energy cost per move
REPRODUCTION_LIMIT = 10  # Maximum number of times an organism can reproduce
MATING_COOLDOWN = 2  # Cooldown period after mating (in cycles)
MIN_MATING_AGE = 3  # Minimum age before an organism can mate

# Queue to handle AI responses
ai_response_queue = Queue()

# Function to get evolution data from Ollama API
def get_evolution_data(prompt, organism_id):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemma:2b-instruct",  # Specify the model you want to use
        "prompt": prompt,
        "max_tokens": 100
    }
    try:
        response = requests.post(OLLAMA_ENDPOINT, headers=headers, data=json.dumps(data), stream=True)
        response.raise_for_status()
        evolution_text = ""
        for line in response.iter_lines():
            if line:
                try:
                    decoded_line = json.loads(line.decode('utf-8'))
                    evolution_text += decoded_line.get("response", "")
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
        ai_response_queue.put((organism_id, {"choices": [{"text": evolution_text}]}))
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        ai_response_queue.put((organism_id, None))

class Food:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = 5

    def draw(self, screen):
        # Draw a small green square to represent food
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.size, self.size))

class Organism:
    def __init__(self, x, y, size=5, color=PINK, genetic_traits=None, energy=INITIAL_ENERGY):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.age = 0
        self.lifespan = random.randint(50, LIFESPAN_LIMIT)
        self.food_eaten = 0
        self.energy = energy
        self.reproductions = 0
        self.mated = False  # Flag to indicate if the organism has mated
        self.mating_cooldown = 0  # Cooldown timer for mating
        self.target = None  # Current target for movement (food or mate)
        self.random_direction = (random.choice(["up", "down", "left", "right"]), random.randint(10, 50))  # Random direction and steps to move
        self.last_position = (self.x, self.y)  # Store the last position to check for movement
        if genetic_traits is None:
            self.genetic_traits = {
                "speed": random.uniform(1, 2),  # Increased minimum speed
                "size_limit": random.randint(5, SIZE_LIMIT),
                "reproduction_threshold": random.randint(1, REPRODUCTION_FOOD_THRESHOLD),
                "color": color  # Initial color
            }
        else:
            self.genetic_traits = genetic_traits
        self.id = id(self)
        self.evolving = False
        self.evolution_result = None

    def move(self, direction=None):
        move_distance = 1 * self.genetic_traits["speed"]
        if direction == "up":
            self.y = (self.y - move_distance) % HEIGHT
        elif direction == "down":
            self.y = (self.y + move_distance) % HEIGHT
        elif direction == "left":
            self.x = (self.x - move_distance) % WIDTH
        elif direction == "right":
            self.x = (self.x + move_distance) % WIDTH
        else:
            # Ensure random movement is not too small
            self.x = (self.x + random.randint(-5, 5) * move_distance) % WIDTH
            self.y = (self.y + random.randint(-5, 5) * move_distance) % HEIGHT
        self.energy -= ENERGY_COST
        if self.energy <= 0:
            self.die()

        # Check if the organism has moved from its last position
        if (self.x, self.y) == self.last_position:
            # If not, give it a nudge in a random direction
            self.move(random.choice(["up", "down", "left", "right"]))
        else:
            self.last_position = (self.x, self.y)  # Update the last position

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        dx, dy = dx / dist, dy / dist
        self.x += dx * self.genetic_traits["speed"]
        self.y += dy * self.genetic_traits["speed"]
        self.energy -= ENERGY_COST / 2  # Less energy cost when moving towards food or other organisms
        if self.energy <= 0:
            self.die()

        # Check if the organism has moved from its last position
        if (self.x, self.y) == self.last_position:
            # If not, give it a nudge in a random direction
            self.move(random.choice(["up", "down", "left", "right"]))
        else:
            self.last_position = (self.x, self.y)  # Update the last position

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def check_collision(self, other):
        return math.hypot(self.x - other.x, self.y - other.y) < self.size + other.size

    def eat(self, food):
        if self.energy < INITIAL_ENERGY:  # Only eat if not at full energy
            self.size = min(self.size + 1, self.genetic_traits["size_limit"])
            self.food_eaten += 1
            self.energy += ENERGY_GAIN
            if self.energy > INITIAL_ENERGY:
                self.energy = INITIAL_ENERGY
            print(f"Organism at ({self.x}, {self.y}) ate food. Size: {self.size}, Energy: {self.energy}")

    def die(self):
        if self in organisms:
            organisms.remove(self)
        print(f"Organism at ({self.x}, {self.y}) died.")

    def mutate(self):
        new_traits = self.genetic_traits.copy()
        # Ensure offspring has a different color than the parent
        while new_traits["color"] == self.color:
            new_traits["color"] = (
                min(255, max(0, self.color[0] + random.randint(-50, 50))),
                min(255, max(0, self.color[1] + random.randint(-50, 50))),
                min(255, max(0, self.color[2] + random.randint(-50, 50)))
            )
        # Randomly mutate one other trait
        mutation_choice = random.choice(["speed", "size_limit", "reproduction_threshold"])
        if mutation_choice == "speed":
            new_traits["speed"] = max(0.1, new_traits["speed"] + random.uniform(-0.1, 0.1))
        elif mutation_choice == "size_limit":
            new_traits["size_limit"] = max(1, new_traits["size_limit"] + random.randint(-1, 1))
        elif mutation_choice == "reproduction_threshold":
            new_traits["reproduction_threshold"] = max(1, new_traits["reproduction_threshold"] + random.randint(-1, 1))
        return new_traits

    def request_evolution(self, food):
        prompt = f"Simulate the next step in the evolution of this organism:\n"
        prompt += f"Organism: size={self.size}, color={self.color}, position=({self.x}, {self.y}), age={self.age}, lifespan={self.lifespan}, food_position=({food.x}, {food.y}), genetic_traits={self.genetic_traits}\n"
        prompt += "Choose the action you think is most beneficial to the organism in its environment: grow, shrink, change color, reproduce, move up, move down, move left, move right, move towards food."
        
        threading.Thread(target=get_evolution_data, args=(prompt, self.id)).start()
        self.evolving = True

    def evolve(self):
        if not self.evolving:
            return None
        self.evolving = False
        evolution_data = self.evolution_result
        if not evolution_data:
            return None
        choices = evolution_data.get("choices", [])
        if choices:
            text = choices[0].get("text", "").strip().lower()
            print(f"Organism at ({self.x}, {self.y}) chose to {text}")
            if "grow" in text and self.size < self.genetic_traits["size_limit"]:
                self.size += 1
            elif "shrink" in text:
                self.size = max(1, self.size - 1)
            elif "change color" in text:
                self.color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            elif "reproduce" in text and self.food_eaten >= self.genetic_traits["reproduction_threshold"]:
                return self.reproduce()
            elif "move" in text:
                if "up" in text:
                    self.move("up")
                elif "down" in text:
                    self.move("down")
                elif "left" in text:
                    self.move("left")
                elif "right" in text:
                    self.move("right")
                elif "towards food" in text:
                    closest_food = min(food_sources, key=lambda food: math.hypot(self.x - food.x, self.y - food.y))
                    self.move_towards(closest_food.x, closest_food.y)
        self.age += 1
        self.size = min(self.size + 0.1, self.genetic_traits["size_limit"])  # Grow with age
        return None

    def reproduce(self):
        if self.size >= self.genetic_traits["size_limit"] / 2 and self.reproductions < REPRODUCTION_LIMIT:
            child_size = 1  # Offspring start small
            self.size = min(self.size + REPRODUCTION_BONUS, self.genetic_traits["size_limit"])  # Increase size after reproduction
            self.lifespan += REPRODUCTION_BONUS  # Increase lifespan after reproduction
            self.food_eaten = 0  # Reset food eaten after reproduction
            self.reproductions += 1  # Increment reproduction count
            self.mating_cooldown = MATING_COOLDOWN  # Set mating cooldown
            new_traits = self.mutate()
            self.mated = True  # Set the mated flag to true after reproduction
            print(f"Organism at ({self.x}, {self.y}) reproduced. Child size: {child_size}, New traits: {new_traits}")
            child = Organism(self.x, self.y, size=child_size, color=new_traits["color"], genetic_traits=new_traits)
            # Give the child a random direction to move in
            child.move(random.choice(["up", "down", "left", "right"]))
            return child
        return None

    def update_mating_cooldown(self):
        if self.mating_cooldown > 0:
            self.mating_cooldown -= 1

    def update_target(self, food_sources, organisms):
        # If there's no target or the target is food that has been eaten, find a new target
        if self.target is None or (isinstance(self.target, Food) and (self.target not in food_sources or self.energy >= INITIAL_ENERGY)):
            # Prioritize food first
            if self.energy < INITIAL_ENERGY:
                closest_food = min(food_sources, key=lambda food: math.hypot(self.x - food.x, self.y - food.y), default=None)
                if closest_food:
                    self.target = closest_food
            # Only target another organism for mating if conditions allow and no food is targeted
            if self.target is None and self.age >= MIN_MATING_AGE and self.mating_cooldown == 0:
                potential_mates = [org for org in organisms if org != self and org.age >= MIN_MATING_AGE and org.mating_cooldown == 0]
                closest_mate = min(potential_mates, key=lambda org: math.hypot(self.x - org.x, self.y - org.y), default=None)
                if closest_mate:
                    self.target = closest_mate

        # If still no target, move randomly
        if self.target is None:
            if self.random_direction[1] > 0:
                self.move(self.random_direction[0])
                self.random_direction = (self.random_direction[0], self.random_direction[1] - 1)
            else:
                self.random_direction = (random.choice(["up", "down", "left", "right"]), random.randint(10, 50))
        # If targeting food, move towards it
        elif isinstance(self.target, Food):
            self.move_towards(self.target.x, self.target.y)
        # If targeting a mate, move towards it
        elif isinstance(self.target, Organism):
            self.move_towards(self.target.x, self.target.y)
            if self.check_collision(self.target):
                new_organism = self.reproduce()
                if new_organism and len(organisms) < POPULATION_LIMIT:
                    organisms.append(new_organism)
                self.mated = True  # Reset mated flag after reproduction
                self.target.mated = True  # Reset mated flag for the other organism
                self.mating_cooldown = MATING_COOLDOWN  # Reset mating cooldown
                self.target.mating_cooldown = MATING_COOLDOWN  # Reset mating cooldown for the other organism

def handle_ai_responses():
    while not ai_response_queue.empty():
        organism_id, response = ai_response_queue.get()
        for organism in organisms:
            if organism.id == organism_id:
                organism.evolution_result = response

def main():
    global organisms, food_sources
    clock = pygame.time.Clock()
    organisms = [Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(20)]
    food_sources = [Food() for _ in range(FOOD_COUNT)]
    running = True
    last_evolution_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Update and draw organisms
        for organism in organisms[:]:
            organism.update_target(food_sources, organisms)
            organism.draw(screen)
            if isinstance(organism.target, Food) and organism.check_collision(organism.target):
                organism.eat(organism.target)
                food_sources.remove(organism.target)
                food_sources.append(Food())  # Respawn food at a new location
                organism.target = None  # Clear target after eating

            if organism.age > organism.lifespan:
                organisms.remove(organism)

            organism.update_mating_cooldown()  # Update mating cooldown

        # Draw food sources
        for food in food_sources:
            food.draw(screen)

        pygame.display.flip()
        clock.tick(30)

        # Handle AI responses
        handle_ai_responses()

        # Simulate evolution every 5 seconds
        if time.time() - last_evolution_time > 5:
            for organism in organisms[:]:
                if organism.food_eaten >= organism.genetic_traits["reproduction_threshold"] and not organism.evolving:  # Only evolve if the organism has eaten enough food and is not already evolving
                    closest_food = min(food_sources, key=lambda food: math.hypot(organism.x - food.x, organism.y - food.y))
                    organism.request_evolution(closest_food)
                new_organism = organism.evolve()
                if new_organism and len(organisms) < POPULATION_LIMIT:
                    organisms.append(new_organism)
            last_evolution_time = time.time()

    pygame.quit()

if __name__ == "__main__":
    main()
