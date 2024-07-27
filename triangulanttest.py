# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 23:48:56 2024

@author: gelbo
"""

from triangulant import lattice
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.stats import norm
plt.rcParams['font.size']=15


'''settings:'''
plots = True
draw = True
time = 100
speed = 80 #0 to 99
saw = False #he may get trapped :(



'''presets:'''
a = 10
h = np.sqrt(a**2 - (a/2)**2)
# lattice.build([a/2,h], [a,0], a*10, 'hexagonal', saw=saw, speed=speed)

lattice.build([1,0], [0,1], 100, 'square', saw=saw, speed=speed)



'''run:'''
ant = lattice.generant()
if draw == True:
    ant.draw()

runcount = 0
for i in np.arange(0,time):
    try:
        ant.move(1)
        if draw == True:
            ant.update()
        runcount += 1
        # print(runcount)
    except KeyboardInterrupt:
        break
plt.close('all')



'''stats:'''
if plots==False:
    sys.exit()

def gauss(x, mu, sgma):
    y = (1/((sgma**2)*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sgma)**2)
    return y

def travelstats(ltm, N): #statistics of displacement after N steps
    dist = []
    for i in np.arange(0, len(ltm) - N):
        p1 = ltm[i]
        p2 = ltm[i+N]
        dx = abs(p1[1] - p2[1])
        dy = abs(p1[0] - p2[0])
        hyp = np.sqrt(dx**2 + dy**2)
        dist.append(hyp)
    mu = np.mean(dist)
    sigma = np.std(dist)
    return dist, mu, sigma

travelled, mu, sigma = travelstats(ant.ltm, 5)

bins = np.linspace(0, np.max(travelled), 5)
gaussx = np.linspace(0, np.max(travelled), 100)
style={'facecolor': 'pink'}

fig = plt.figure(figsize=(10,10))
plt.hist(travelled, bins=5, density='True', **style)
plt.plot(gaussx, gauss(gaussx, mu, sigma), label = f'mu = {mu:.3f}, sigma = {sigma:.3f}')
plt.title('Distribution of step sizes')
plt.xlabel('Step length')
plt.ylabel('Number of times taken')
plt.grid()
plt.legend()
plt.show()

var = []
for j in np.arange(1,int(runcount/2)):
    trav, mu, sigma = travelstats(ant.ltm, j)
    v = sigma**2
    var.append(v)
    print(j)
fig = plt.figure()
plt.plot(np.arange(1,int(runcount/2)), var)
plt.xlabel('Number of steps')
plt.ylabel('Variance')
plt.show()