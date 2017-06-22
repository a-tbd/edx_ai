'''
Perceptron Learning Algorithm
Input: CSV set of linearly seperable datapoints (x, y, classification)
Output: CSV set of weights for each datapoint (w_1, w_2, bias)
'''
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import itertools
import pdb
import sys
import csv


class Perceptron(object):
    def __init__(self, inp, out):
        self.input = inp
        self.output = out
        self.features = []
        self.weights = [0,0,0]
        self.prev_w = None
        self.figure = 0

    def set_features(self):
        self.features = [map(int,i) for i in csv.reader(open('input1.csv'))]
    
    def predict(self):
    	out = open(self.output, 'a+')
    	# repeat until convergence
        while self.prev_w != self.weights:
            self.update_weights()
            format = [str(self.weights[0]), str(self.weights[1]), str(self.weights[2])]
            out.write((',').join(format) + '\n')
            self.visualize()
        out.close()

    def update_weights(self):
        cycle = itertools.cycle(self.features)
        self.prev_w = [i for i in self.weights]
        for i in range(len(self.features)):
            row = next(cycle)
            e = self.error(row)
            if e != row[-1]:
                for i in range(len(self.weights) - 1):
                    self.weights[i] += row[-1]*row[i]
                self.weights[2] += row[-1]
	
    def error(self, row):
        activation = 0
        #pdb.set_trace()
        for i in range(len(row) - 1):
            activation += self.weights[i] * row[i] 
        return 1 if activation > -self.weights[2] else -1

    def visualize(self):
        filename = '%d.png' % self.figure
        trans = np.transpose(self.features)
        colors = ['.10' if i < 0 else '.90' for i in trans[2]]
        for i in range(len(colors)):
            plt.scatter(trans[0][i], trans[1][i], color=colors[i])
        if not self.weights[0] is 0 and not self.weights[1] is 0:
            (m, b) = pl.polyfit([0, -self.weights[2]/self.weights[0]], [-self.weights[2]/self.weights[1], 0], 1)
            yp = pl.polyval([m,b], trans[0])
            plt.plot(trans[0], yp)
            plt.savefig(filename, dpi=None, facecolor='w', edgecolor='w',
                              orientation='portrait', papertype=None, format=None,
                              transparent=False, bbox_inches=None, pad_inches=0.1,
                              frameon=None)
        plt.cla()
        self.figure += 1

def main(argv):
    try:
        inp, out = argv
    except:
        print 'useage: problem1.py input1.csv output.csv'
        sys.exit(2)
    
    open(out, 'w').close()
    p = Perceptron(inp, out)
    p.set_features()
    p.predict()


if __name__ == "__main__":
    main(sys.argv[1:])
