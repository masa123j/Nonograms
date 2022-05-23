class Resitev (object):

    def __init__(self, podanoStanje, podaniFitness):
        self.stanje = podanoStanje
        self.fitness = podaniFitness

    def __cmp__(self, other):
        if self.fitness < other.fitness:
            return -1
        elif self.fitness > other.fitness:
            return 1
        else:
            return 0

    def dobiStanje (self):
        return self.stanje

    def dobiFitness (self):
        return self.fitness