#!/home/ann/anaconda3/bin/python

# Ref:
# http://www.meetup.com/Palo-Alto-Data-Science-Association/events/220701369/
# http://continuum.io/downloads#py34

# Demo:
# cd ~ann
# vi py102.py
# ~ann/anaconda3/bin/python py102.py

# Your homework is to type the questions into Google and study the answers.

# This script should work with a CSV file created by py101.py

import pandas as pd
import numpy  as np
import pdb

df2 = pd.read_csv('df2.csv')

# q: In Python how to fill NumPy array column with a List?
elements = np.arange(0,10);
colstrings = list();
for elem in elements:
	order = 2**elem;
	colstrings = colstrings + ['lag'+str(order)+'_pctg'];
nrows = len(df2[['cp']].values);
ncols = len(colstrings);
crop = 2**(elements[-1]+1); # to crop out the range where some of the lead and lag have no good values
xvalues = (df2[colstrings].values)[crop:-crop, :];
#temp = (df2[['lead1_pctg']].values)[:,0]; # UGH... again this doesn't return the single vector, but a 2D thing that is N by 1 shaped.
yvalues = (df2[['lead1_pctg']].values)[crop:-crop, 0]; # So this is how you do it... 
yclasses = yvalues > 0.0;

# q: In Python what commands does pdb offer me in its UI?
# pdb.set_trace()

# q: In Python, NumPy how to get row-0 from Array?
x_oos = xvalues[0,:]

# q: In Python, NumPy how to get row-1 through row-1000 from Array?
x_is  = xvalues[1:1001,:]
y_is  = yclasses[1:1001 ]
# q: In Machine Learning what is difference between
#    Out OF Sample (OOS) and In Sample (IS) X values?

# q: In Python scikit-learn, what is KNeighborsClassifier?
from sklearn.neighbors import KNeighborsClassifier

# q: In scikit-learn, when I build a KNeighborsClassifier object,
#    what is n_neighbors? what is weights?
knn = KNeighborsClassifier(n_neighbors=len(y_is), weights='distance')

# q: In scikit-learn, when I build a KNeighborsClassifier object,
#    what does the fit() method do?
knn.fit(x_is, y_is)
# Why does the fit() method take two arguments?

print('I have just learned from '+str(len(y_is))+' observations.')

# q: In scikit-learn, when I build a KNeighborsClassifier object,
#    what does the predict_proba() method do?
upprob = knn.predict_proba(x_oos)[0,1]
# Why does it take one argument?

print('Probability that lead_pctg will be > 0')
print('For these x-values:')
print(x_oos)
print('is: ')
print(100.0 * upprob)
print('percent')

# done
