#!/home/ann/anaconda3/bin/python

import subprocess as sp;
import numpy as np;
import pandas as pd;
import pdb;
from collections import deque;

sp.call(['/bin/date']);
tkrh='%5EGSPC';
tkr ='GSPC';
tkrfile = tkr+'.csv';
#sp.call(['/bin/rm', '-f',tkrfile]);

cmd  = "/usr/bin/wget";
arg0 = "-nc";
arg1 = "--output-document="+tkrfile;
arg2 = "http://ichart.finance.yahoo.com/table.csv?s="+tkrh;
sp.call([cmd,arg0,arg1,arg2]);
#sp.call(["/usr/bin/head", tkrfile]);
df1 = pd.read_csv(tkr+'.csv');
#print(df1.head());
#print("\n\n");
#print(df1.tail());
df2 = df1[['Date','Close']];
df2.columns = ['cdate','cp'];
#print (df2.head())

maxlen = len(df2[['cdate']]); # using maxlen to restrict the deque # second thought, just use the deque.rotate(bynum) method
#print(maxlen);
dqDate = deque(df2[['cdate']].values,maxlen);

dqCp = deque(df2[['cp']].values,maxlen);
dqCp.rotate(-1);
temp = [record[0] for record in dqCp]; # this feels like a hack... confusing type casting
df2['cplag'] = temp;
dqCp.rotate(-1);
temp = [record[0] for record in dqCp]; # this feels like a hack... confusing type casting
df2['cplag2'] = temp;
dqCp.rotate(+3);
temp = [record[0] for record in dqCp]; # this feels like a hack... confusing type casting
df2['cplead'] = temp;
dqCp.rotate(+1);
temp = [record[0] for record in dqCp]; # this feels like a hack... confusing type casting
df2['cplead2'] = temp;

df2['lag_pctg'] = 100.* (df2[['cp']].values - df2[['cplag']].values)/( ( df2[['cp']].values + df2[['cplag']].values) / 2.); 
df2['lead_pctg'] = 100.* (df2[['cp']].values - df2[['cplead']].values)/( ( df2[['cp']].values + df2[['cplead']].values) / 2.);
df2['lag2_pctg'] = 100.* (df2[['cp']].values - df2[['cplag2']].values)/( ( df2[['cp']].values + df2[['cplag2']].values) / 2.); 
df2['lead2_pctg'] = 100.* (df2[['cp']].values - df2[['cplead2']].values)/( ( df2[['cp']].values + df2[['cplead2']].values) / 2.);

#print(df2.head())

df2.to_csv('df2.csv', float_format='%4.3f', index=False);
