# -*- coding: utf-8 -*-
"""FoDS A1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hfBGPZsWq7Q0vsw4JfZRipQqatnQnRiT
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy
import random
from scipy.stats import beta
import matplotlib as mp
mp.rcParams.update({'figure.max_open_warning': 0})

dataset_1 = [1]*55
dataset_0 = [0]*105
dataset = dataset_1+dataset_0

random.shuffle(dataset)

print("The randomly genereated dataset is as follows = ", dataset)

a = 4
b = 6
x = np.linspace(0, 1, 1002)[1:-1]
fig, ax = plt.subplots(figsize=(5, 3.75))
dist = beta(a, b)
plt.plot(x, dist.pdf(x), c='black', label=r'$\alpha=%.1f,\ \beta=%.1f$' % (a, b))

plt.xlim(0, 1)
plt.ylim(0, 3)

plt.xlabel('$x$')
plt.ylabel(r'$p(x|\alpha,\beta)$')
plt.title('Beta Distribution with mean of prior = 0.4')

plt.legend(loc=0)
plt.show()

a = 4+55
b = 6+105
x = np.linspace(0, 1, 1002)[1:-1]
fig, ax = plt.subplots(figsize=(5, 3.75))
dist = beta(a, b)
plt.plot(x, dist.pdf(x), c='black', label=r'$\alpha=%.1f,\ \beta=%.1f$' % (a, b))

plt.xlabel('$x$')
plt.ylabel(r'$p(x|\alpha,\beta)$')
plt.title('Beta Distribution')

plt.legend(loc=0)
plt.show()

a = 4
b = 6

for i in range(len(dataset)):
  cur = dataset[i]
  if(cur == 1):
    a += 1
  else:
    b += 1
  x = np.linspace(0, 1, 1002)[1:-1]
  fig, ax = plt.subplots(figsize=(5, 3.75))
  dist = beta(a, b)
  plt.plot(x, dist.pdf(x), c='black', label=r'$\alpha=%.1f,\ \beta=%.1f$' % (a, b))

  plt.xlabel('$x$')
  plt.ylabel(r'$p(x|\alpha,\beta)$')
  plt.title('Beta Distribution')

  plt.legend(loc=0)
  plt.savefig("./GIF Images/"+str(i)+".png")
