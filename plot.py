import matplotlib.pyplot as plt
import numpy as np

def read_file(filename):
    with open(filename) as inputfile:
        for line in inputfile:
            print(line[0])

y = [i for i in range(20,100,3)]
x = [i for i in range(len(y))]

read_file("processor")

#plt.plot(x,y)
#plt.show()
