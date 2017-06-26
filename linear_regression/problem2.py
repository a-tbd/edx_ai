'''
Linear Regression using Gradient Descent

Input: CSV of ordered triples (age, weight, height)
Output: CSV of weights (alpha, number_of_iterations, b_0, b_age, b_weight)

Helpful link: http://www.holehouse.org/mlclass/04_Linear_Regression_with_multiple_variables.html
'''
import sys
import numpy as np
import csv
import itertools

CONDITIONS = [(0.001,100), 
              (0.005,100), 
              (0.01,100), 
              (0.05,100), 
              (0.1,100), 
              (0.5,100), 
              (1.,100), 
              (5.,100), 
              (10.,100), 
              (.75,1000)]

class LinearRegression(object):
    def __init__(self, inp, out, iterations, weights=None):
        self.input = inp
        self.output = out
        self.iterations = iterations
        self.weights = weights or [0.0,0.0,0.0]
        self.data = None
        self.features = None
        self.labels = None

    def get_data(self):
        self.data = [map(float,i) for i in csv.reader(open(self.input))]

    def scale_data(self):
        # new array = (x_i - mean) / stdv
        sd = np.std(self.data, axis=0)
        mean = np.mean(self.data, axis=0)
        trans = np.transpose(self.data)
        scaled = [np.divide([np.subtract(trans[i], j) 
                       for i, j in enumerate(mean)][n], m) 
                       for n, m in enumerate(sd)]
        return np.concatenate((scaled[0:2], [np.transpose(self.data)[-1]]), axis=0)

    def set_features_labels(self):
        self.get_data()
        scaled = self.scale_data()
        ones_data = np.append([np.ones(len(self.data))], scaled, axis=0)
        self.features = np.transpose(ones_data[:-1])
        self.labels = np.transpose(ones_data[-1])
    
    def predict_next(self, rate):
        for i in range(self.iterations):
            error = np.dot(self.features, self.weights) - self.labels
            error_j = np.transpose([[error[i] * self.features[i][j] 
                                    for j in range(len(self.weights))] 
                                    for i in range(len(self.features))])
            for i in range(len(self.weights)):
                self.weights[i] -= rate*(1./len(self.features))*sum(error_j[i])
        self.outprocess(rate)

    def outprocess(self, rate):
        out = open(self.output, 'a+')
        output_data = map(str,([rate, self.iterations] + self.weights))
        out.write(','.join(output_data) + '\n')
    
def main(argv):
    try:
        inp, out = argv
    except:
        print 'useage: problem2.py input2.csv output2.csv'
        sys.exit(2)
    
    open(out, 'w').close()
    for c in CONDITIONS:
    	rate, iterations = c
        lr = LinearRegression(inp, out, iterations, [0.0,0.0,0.0])
        lr.set_features_labels()
        lr.predict_next(rate)

if __name__ == "__main__":
    main(sys.argv[1:])


