import random

class ReplayMemory():  # iNstead of using array try using doubly linked list - orderedDict
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.push_count = 0  # keep track of how many experiences we've added to memory

    # function to store experiences as they occur in replay memory
    def push(self, experience):
        if len(self.memory) < self.capacity:
            self.memory.append(experience)
        else:
            # if number of experiences exceeds capacity,
            # push the new experience to the front of memory, overriding the oldest experiences
            self.memory[self.push_count % self.capacity] = experience
        self.push_count += 1

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def can_provide_sample(self, batch_size):
        return len(self.memory) >= batch_size

