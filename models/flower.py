import random
class Blossom:
    def __init__(self, pos, name, color):
        self.pos = pos
        self.name = name
        self.color = color
        self.nectar = random.choice([0, 1, 2, 3])  # Allow empty flowers

    def harvest(self):
        if self.nectar > 0:
            self.nectar -= 1
            return 1
        return 0

