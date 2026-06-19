class Hive:
    def __init__(self, position, honey_level=0, max_capacity=50):
        self.position = position
        self.honey_level = honey_level
        self.max_capacity = max_capacity
        self.flower_knowledge = set()
        self.signals = []

    def deposit(self, nectar):
        self.honey_level = min(self.honey_level + nectar, self.max_capacity)

    def get_nectar_level(self):
        return self.honey_level

    def get_flower_locations(self):
        return list(self.flower_knowledge)

