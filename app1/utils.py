__author__ = 'soheil'
import random
def get_random_index(probabilities):
    prob_sum = sum(probabilities)
    rand_idx = random.randrange(0, prob_sum)
    total = 0
    for idx, x in enumerate(probabilities):
        total += x
        if rand_idx < total:
            return idx
