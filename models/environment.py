import numpy as np
from models.hive import Hive
from models.bee import WorkerBee
from models.flower import Blossom
from models.terrain import Obstacle

class Environment:
    def __init__(self, area_size, bee_count, flower_count, obstacle_count, steps, communication, terrain=None):
        self.size = area_size
        self.bee_count = bee_count
        self.flower_count = flower_count
        self.obstacle_count = obstacle_count
        self.steps = steps
        self.communication = communication
        self.terrain = terrain if terrain is not None else np.zeros((area_size, area_size), dtype=int)
        self.bees = []
        self.flowers = []
        self.obstacles = []
        self.hive = None
        self.time = 0

    def initialize(self):
        # Place hive at center
        hive_pos = (self.size // 2, self.size // 2)
        self.hive = Hive(hive_pos, honey_level=0)
        # Place flowers
        for i in range(self.flower_count):
            while True:
                pos = (np.random.randint(0, self.size), np.random.randint(0, self.size))
                if self.terrain[pos] == 0 and pos != hive_pos and all(f.pos != pos for f in self.flowers):
                    self.flowers.append(Blossom(pos, name=f"Flower{i+1}", color="yellow"))
                    break
        # Place obstacles
        for _ in range(self.obstacle_count):
            while True:
                pos = (np.random.randint(0, self.size), np.random.randint(0, self.size))
                if self.terrain[pos] == 0 and pos != hive_pos and all(f.pos != pos for f in self.flowers) and all(o.pos != pos for o in self.obstacles):
                    self.obstacles.append(Obstacle(pos))
                    self.terrain[pos] = 9  # 9 = obstacle
                    break
        # Place bees in hive
        for i in range(self.bee_count):
            self.bees.append(WorkerBee(f"bee_{i}", self.hive, self.communication))

    def update(self):
        self.time += 1
        for bee in self.bees:
            bee.step(self)

    def flower_at(self, pos):
        for flower in self.flowers:
            if flower.pos == pos:
                return flower
        return None

