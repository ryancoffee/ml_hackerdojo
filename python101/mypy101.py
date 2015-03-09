#!/home/ann/anaconda3/bin/python

import subprocess as sp;
import numpy as np;
import pandas as pd;
import pdb;
from collections import deque;
from scipy import signal

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
df1 = pd.read_csv(tkr+'.csv');
df2 = df1[['Date','Close']];
df2.columns = ['cdate','cp'];

maxlen = len(df2[['cdate']]); # using maxlen to restrict the deque # second thought, just use the deque.rotate(bynum) method
#dqDate = deque(df2[['cdate']].values,maxlen);
#dqCp = deque(df2[['cp']].values,maxlen);
#temp = [record[0] for record in dqCp]; # this feels like a hack... confusing type casting
freqs = np.arange(0,0.5,1./float(maxlen/2)) 
fft1 = np.fft.rfft( df2[['cp']].values )/float(maxlen/2)
fft2 = (abs(fft1)**2)/float(len(fft1)/2)
conv = np.fft.ifft(fft1*fft1);
#df = zip(np.real(conv),np.imag(conv));
#conv_df= pd.DataFrame(df,columns=['Real', 'Imag']);
np.savetxt('fft.dat',fft2,'%.4f',',');
np.savetxt('conv.real.dat',np.real(conv),'%.4f',',');
np.savetxt('conv.imag.dat',np.imag(conv),'%.4f',',');
#conv_df.to_csv('conv.csv', float_format='%4.3f', index=False);
#np.savetxt('conv.dat',conv,'%.4f',',');

#dqCp.rotate(-1);
#temp = [record[0] for record in dqCp]; # this feels like a hack... confusing type casting
#df2['cplag'] = temp;
cp = df2[['cp']].values; # this .values method returns the numpy array

temp = np.roll(cp,1);
df2['lead1_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-1);
df2['lag1_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-2);
df2['lag2_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-4);
df2['lag4_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-8);
df2['lag8_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-16);
df2['lag16_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-32);
df2['lag32_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-64);
df2['lag64_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-128);
df2['lag128_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-256);
df2['lag256_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;
temp = np.roll(cp,-512);
df2['lag512_pctg'] = 100.*( cp - temp)/(cp + temp)*2.0;

df2.to_csv('df2.csv', float_format='%4.3f', index=False);
