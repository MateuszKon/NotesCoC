from datetime import datetime
from random import SystemRandom

import matplotlib.pyplot as plt
import numpy as np

NUMBER_OF_ROLLS = 10000

rng = SystemRandom()

hist = {i: 0 for i in range(1, 11)}
current = hist.get
for i in range(NUMBER_OF_ROLLS):
    roll = rng.randint(1, 10)
    hist[roll] = current(roll, 0) + 1

print(hist.values())

lists = sorted(hist.items()) # sorted by key, return a list of tuples
x, y = zip(*lists)  # unpack a list of pairs into two tuples
for x, y in lists:
    plt.bar(x, y)
plt.axhline(NUMBER_OF_ROLLS/10)
m = np.sum([key * value for key, value in hist.items()]) / NUMBER_OF_ROLLS
plt.text(0.6, 0, m)
plt.show()