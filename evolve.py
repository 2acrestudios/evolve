import random
import pygame
import sys
import threading
import requests
import json
from queue import Queue, Empty

SCREEN_SIZE = (800, 600)
BG_COLOR = (0, 0, 0)
DEFAULT_ENTITY_COLOR = (230, 225, 200)
MUTATION_RATE = 0.2
STARTING_ENTITIES = 50
MAX_SPEED = 10
COLOR_MUTATION_RATE = 30
REPRODUCTION_LIMIT = 3
MAX_POPULATION = 500
REPRODUCTION_COOLDOWN = 300
LIFESPAN = 500
AI_ENDPOINT = "http://localhost:11434/api/generate"
MODEL = 'gemma:2b-instruct'

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
decision_queue = Queue()

class Entity:
    def __init__(self, x, y, size=3, speed=1, color=DEFAULT_ENTITY_COLOR, reproduction_limit=REPRODUCTION_LIMIT, lifespan=LIFESPAN):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.decision = "move"
        self.reproductions = 0
        self.reproduction_limit = reproduction_limit
        self.reproduction_cooldown = 0
        self.lifespan = lifespan

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def decide_action(self):
        try:
            self.decision = decision_queue.get_nowait()
        except Empty:
            pass

    def act_based_on_decision(self):
        if self.lifespan <= 0:
            return 'die'
        self.lifespan -= 1
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1
        if self.decision == "move":
            self.move()
        elif self.decision == "reproduce" and self.reproduction_cooldown == 0:
            return self.reproduce()
        return None

    def move(self):
        self.x += random.randint(-self.speed, self.speed)
        self.y += random.randint(-self.speed, self.speed)
        self.x = min(max(self.x, 0), SCREEN_SIZE[0])
        self.y = min(max(self.y, 0), SCREEN_SIZE[1])

    def reproduce(self, partner=None):
        global entities

        if len(entities) >= MAX_POPULATION or self.reproductions >= self.reproduction_limit or self.reproduction_cooldown > 0:
            return None

        base_color = self.color if not partner else tuple(
            (sc + pc) // 2 for sc, pc in zip(self.color, partner.color)
        )
        new_color = tuple(
            min(255, max(0, component + random.randint(-COLOR_MUTATION_RATE, COLOR_MUTATION_RATE)))
            for component in base_color
        )
        child_size = max(1, self.size + random.choice([-1, 1]))
        child_speed = min(MAX_SPEED, max(1, self.speed + random.choice([-1, 1])))
        child_x = min(max(self.x + random.randint(-20, 20), 0), SCREEN_SIZE[0])
        child_y = min(max(self.y + random.randint(-20, 20), 0), SCREEN_SIZE[1])

        self.reproductions += 1
        self.reproduction_cooldown = REPRODUCTION_COOLDOWN

        return Entity(child_x, child_y, child_size, child_speed, new_color, self.reproduction_limit)

    def is_touching(self, other):
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return distance < (self.size + other.size)

def fetch_decision_from_ai():
    while True:
        try:
            response = requests.post(AI_ENDPOINT, json={'model': MODEL, 'prompt': 'Next action?'}, timeout=5)
            response.raise_for_status()
            for line in response.text.splitlines():
                try:
                    decision_data = json.loads(line)
                    decision = decision_data.get('decision', 'move')
                    decision_queue.put(decision)
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
        except requests.RequestException as e:
            print(f"Error fetching decision from AI: {e}")

def main_loop():
    global entities
    entities = [Entity(random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]),
                       size=random.randint(1, 4), speed=random.randint(1, MAX_SPEED))
                for _ in range(STARTING_ENTITIES)]

    clock = pygame.time.Clock()
    threading.Thread(target=fetch_decision_from_ai, daemon=True).start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BG_COLOR)

        for entity in entities[:]:
            outcome = entity.act_based_on_decision()
            if outcome == 'die':
                entities.remove(entity)
            else:
                entity.draw()

        new_entities = []
        for i, entity in enumerate(entities):
            for other in entities[i+1:]:
                if entity.is_touching(other):
                    offspring = entity.reproduce(other)
                    if offspring:
                        new_entities.append(offspring)

        entities.extend(new_entities)
        entities = entities[:MAX_POPULATION]
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main_loop()
