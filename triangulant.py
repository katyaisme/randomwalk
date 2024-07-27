# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 23:28:51 2024

@author: gelbo
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colours

class lattice:
    
    bases = ['hexagonal', 'square']
    
    @classmethod
    def build(cls, a, b, end, basis, saw, speed): #a, b are lattice vectors
    
        '''assertions'''    
        assert speed>=0, "Too slow..."
        assert speed<=99, "Too fast!!!!!"
        assert basis in lattice.bases, f"Please choose a basis out of: {lattice.bases}"
        assert np.shape(a) == (2,), "a should be a list, array or tuple of shape (2,)"
        assert np.shape(b) == (2,), "b should be a list, array or tuple of shape (2,)"
        assert type(saw) == bool, "Set saw to True for a self-avoiding walk, or False for not"
        
        lattice.a = np.array(a)
        lattice.b = np.array(b)
        lattice.end = end
        lattice.basis = basis
        lattice.saw = saw
        lattice.speed = speed
        
    @classmethod
    def generant(cls):
        self = cls.__new__(cls)
        
        self.pos = ([0,0])
        self.stm = ([0,0])
        self.ltm = [[0,0]]
        
        return self
    
    def __str__(self):
        return f'ant at {self.pos[0], self.pos[1]}'
    
    def move(self, N):
        
        if lattice.saw == True:
            assert N == 1, "Sorry, for a self-avoiding walk, step length must be 1 !!"
        
        if lattice.basis == 'square':
            steps = [lattice.a, -lattice.a,
                     lattice.b, -lattice.b]
        
        if lattice.basis == 'hexagonal':
            steps = [lattice.a, -lattice.a,
                     lattice.b, -lattice.b,
                     lattice.a - lattice.b,
                     -lattice.a + lattice.b]
        
        sequ = np.random.choice(np.arange(0,len(steps)), size=N, replace=True)
        
        path = 0
        for i in sequ:
           path += steps[i]
        
        self.pos += path
        
        rounded = list([round(self.pos[0], 4), round(self.pos[1], 4)])
        
        if rounded in self.ltm and lattice.saw==True:
            self.pos = ([self.stm[0], self.stm[1]])
        else:
            self.ltm.append(rounded)
        
    def draw(self):
        self.fig = plt.figure(figsize=(10,10))
        self.ax = self.fig.gca()
        
        self.dot = self.ax.scatter(self.pos[0], self.pos[1], color='k')
        self.ax.set_xlim(-lattice.end,lattice.end)
        self.ax.set_ylim(-lattice.end,lattice.end)
        plt.grid()
        
        self.fig.canvas.draw()
    
    def update(self):
        self.dot.set_offsets([self.pos[0], self.pos[1]])
        
        x = [self.stm[1], self.pos[1]]
        y = [self.stm[0], self.pos[0]]
        self.ax.plot(y, x) #path

        self.stm = ([self.pos[0], self.pos[1]])
        
        self.fig.canvas.draw()
        pause = 1 - (lattice.speed / 100)
        plt.pause(pause)
    