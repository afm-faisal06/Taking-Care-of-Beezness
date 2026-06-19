import numpy as np

class WorkerBee:
    def __init__(self, bee_id, hive, communication):
        self.id = bee_id
        self.hive = hive
        self.position = hive.position
        self.state = "in_hive"  # in_hive, searching, gathering, returning, resting, holding
        self.in_hive = True
        self.carrying_nectar = 0
        self.known_flowers = []
        self.communication = communication
        self.age = 0
        self.target_flower = None
        self.rest_timer = 0

    def step(self, environment):
        self.age += 1

        # Bees rest for first 4 steps
        if self.age <= 4:
            self.state = "resting"
            self.in_hive = True
            return

        if self.state == "resting":
            self.rest_timer -= 1
            if self.rest_timer <= 0:
                self.state = "in_hive"
            return

        if self.state == "in_hive":
            if np.random.rand() < 0.2:
                self.state = "holding"
                self.rest_timer = 2
                return
            self.state = "searching"

        if self.state == "holding":
            self.rest_timer -= 1
            if self.rest_timer <= 0:
                self.state = "searching"
            return

        if self.state == "searching":
            if self.in_hive:
                # Choose a flower to target
                if self.communication == "random" or not self.known_flowers:
                    self.target_flower = np.random.choice(environment.flowers)
                else:
                    known = [f for f in environment.flowers if f.pos in self.known_flowers and f.nectar > 0]
                    self.target_flower = np.random.choice(known) if known else np.random.choice(environment.flowers)
                self.in_hive = False
                if self.target_flower is not None:
                    if self.target_flower.nectar == 0:
                        print(f"Bee {self.id} found empty flower at {self.target_flower.pos}")
                    else:
                        print(f"Bee {self.id} found flower at {self.target_flower.pos}")
                else:
                    print(f"Bee {self.id} did not find a flower to target.")
            if self.target_flower is not None:
                self.move_towards(self.target_flower.pos, environment)
                if self.position == self.target_flower.pos:
                    self.state = "gathering"
            else:
                self.state = "searching"

        elif self.state == "gathering":
            if self.target_flower is not None and self.position == self.target_flower.pos:
                if self.target_flower.nectar > 0:
                    print(f"Bee {self.id} collecting at {self.target_flower.pos}")
                    self.carrying_nectar = self.target_flower.harvest()
                    self.state = "returning"
                    if self.target_flower.pos not in self.known_flowers:
                        self.known_flowers.append(self.target_flower.pos)
                else:
                    print(f"Bee {self.id} found empty flower at {self.target_flower.pos}")
                    self.state = "searching"
                    self.target_flower = None

        elif self.state == "returning":
            self.move_towards(self.hive.position, environment)
            if self.position == self.hive.position:
                self.hive.deposit(self.carrying_nectar)
                self.carrying_nectar = 0
                self.in_hive = True
                self.state = "resting"
                self.rest_timer = 2
                self.share_flower_info(environment)

    def move_towards(self, target, environment):
        dx = np.sign(target[0] - self.position[0])
        dy = np.sign(target[1] - self.position[1])
        new_pos = (self.position[0] + dx, self.position[1] + dy)
        if (0 <= new_pos[0] < environment.size and
            0 <= new_pos[1] < environment.size and
            environment.terrain[new_pos] != 9):
            self.position = new_pos

    def share_flower_info(self, environment):
        if self.target_flower is None:
            return
        if self.communication == "random":
            candidates = [b for b in environment.bees if b.in_hive and b != self]
            if candidates:
                np.random.choice(candidates).known_flowers.extend([self.target_flower.pos])
        elif self.communication == "directed":
            for b in environment.bees:
                if b.in_hive and b != self:
                    b.known_flowers.extend([self.target_flower.pos])

