"""
Split Test Analysis (A/B test)

An A/B test measures the effectiveness of new features introduced into a 
population with a priori statistical significance. In most cases 
This code performs a split test analysis with test data, but also accepts input
from a file in a certain format of (n x 2) CSV. The first row should be the control with a 

conversion, view

tuple or list, and similarly for the rest of the variations. Example:

Sample data

Baseline: 32 conversions out of 595 viewers
Variation 1: 30 conversions out of 599 viewers
Variation 2: 18 conversions out of 622 viewers
Variation 3: 51 conversions out of 606 viewers
Variation 4: 38 conversions out of 578 viewers

stored as 

data = [np.array([32.,595.]),
        np.array([30.,599.]),
        np.array([18.,622.]),
        np.array([51.,606.]),
        np.array([38.,578.])]

The test assumes each view is independent, and binomially distributed with
a true population conversion rate. This allows for a Central Limit Theorem
estimate for statistical significance.

What's your interpretation of these results? What conclusions would you draw? What 
questions would you ask me about my goals and methodology? Do you have any thoughts on the 
experimental design? Please provide statistical justification for your conclusions and 
explain the choices you made in your analysis.

Ricky Kwok, rickyk9487@gmail.com, 2014-10-08."""
#import csv
import numpy as np 
import math
import scipy.stats as stats

class AB_test(object):
    """ Performs an A/B Test with a control (conversion, view) in data[0] 
        and the rest of the variations in data[1:]. """
    def __init__(self, data):
        self._data = data
        self.control = data[0]
        self.test = data[1:]
        return
        
    def unpack(self):
        # Unpacks the data of object self into tuples.
        conversion, view = [], []
        for i in range(np.shape(self.test)[0]):
            conversion.append(self.test[i][0])
            view.append(self.test[i][1])
        return conversion, view
        
    def stats(self):
        """ Computes and returns probabilities, standard errors, Z-scores
            and one-sided p-values resulting from the A/B test. """
        conversion, view = AB_test.unpack(self)
        prob_ctrl = self.control[0]/self.control[1]
        SE_ctrl = math.sqrt(prob_ctrl * (1 - prob_ctrl) / self.control[1])
        prob = np.zeros(len(conversion))
        SE = np.zeros(len(conversion))
        ZScore = np.zeros(len(conversion))
        pvalue = np.zeros(len(conversion))
        for i in range(len(conversion)):
            # probability is the conversion / view, 
            prob[i] = conversion[i]/view[i]
            # SE is \sqrt{ {p (1-p) \over view} } in LaTeX
            SE[i] = math.sqrt(prob[i] * (1-prob[i]) / view[i])
            # Zscore is {p_{test} - p_{control} \over SE_{test} ^ 2 + SE_{control} ^ 2}
            ZScore[i] = (prob[i] - prob_ctrl)/math.sqrt(SE[i] ** 2 + SE_ctrl **2)
            # pvalue is given as the cdf of the normal distribution funcion
            pvalue[i] = stats.norm.cdf(ZScore[i])
        self.prob = prob
        self.se = SE
        self.zscore = ZScore
        self.pvalue = pvalue
        return

    def print_stats(self):
        print "List of ratios of conversion to view: ",
        print self.prob
        print "List of standard errors: ", 
        print self.se
        print "List of Z-scores with corresponding one-sided p-values: "
        print "Z-scores:", self.zscore
        print "p-values:", self.pvalue        
                        
def openfile(filename):
    """ Stores the CSV file into ints and returns a 2D-array."""
    Data = np.genfromtxt(filename, delimiter = ",")
    data = [[]]
    for i in range(np.shape(Data)[0]):
         #Stores information row-by-row
        data.append(Data[i][0:])
    return data

def get_data():
    """ Test data to perform A/B test """
    data = [np.array([32.,595.]),
            np.array([30.,599.]),
            np.array([18.,622.]),
            np.array([51.,606.]),
            np.array([38.,578.])]
    return data

def main():
    """ Gets data, calls class abtest to get stats, then print them."""
    # openfile allows for CSV files with stored data of two columns
    # data = openfile("filename")
    data = get_data()
    abtest = AB_test(data)
    abtest.stats()
    abtest.print_stats()
    
if __name__ == "__main__":
    main()