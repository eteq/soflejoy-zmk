# coding: utf-8
import numpy as np

from copy import deepcopy

from build123d import *

from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
import  numpy as np
from matplotlib import pyplot as plt
get_ipython().run_line_magic('ls', '')
get_ipython().system('cat right_log')
lf=open('right_log').read()
lg
len(lf)
lf
print(lf)
ch0= [l.strip().split('raw_val: ')[-1] for l in lf.split('\n') if 'analog_axis: ch 0' in l]
ch0= [int(l.strip().split('raw_val: ')[-1]) for l in lf.split('\n') if 'analog_axis: ch 0' in l]
ch0= [l.strip().split('raw_val: ')[-1] for l in lf.split('\n') if 'analog_axis: ch 0' in l]
ch0= [l.strip().split('raw_val: ')[-1].replace('\x1b[0m','') for l in lf.split('\n') if 'analog_axis: ch 0' in l]
ch0= [int(l.strip().split('raw_val: ')[-1].replace('\x1b[0m','')) for l in lf.split('\n') if 'analog_axis: ch 0' in l]
ch0= [int(l.strip().split('raw_val: ')[-1].split('\x1b')[0]) for l in lf.split('\n') if 'analog_axis: ch 0' in l]
ch0
ch1= [int(l.strip().split('raw_val: ')[-1].split('\x1b')[0]) for l in lf.split('\n') if 'analog_axis: ch 1' in l]
ch1= np.array([int(l.strip().split('raw_val: ')[-1].split('\x1b')[0]) for l in lf.split('\n') if 'analog_axis: ch 1' in l])
ch0= np.array([int(l.strip().split('raw_val: ')[-1].split('\x1b')[0]) for l in lf.split('\n') if 'analog_axis: ch 0' in l])
ch1
plt.plot(ch1)
plt.plot(ch1, label='x')
plt.clf()
get_ipython().run_line_magic('matplotlib', '')
plt.plot(ch1, label='x')
plt.plot(ch0, label='0')
plt.plot(ch1, label='1')
plt.clf();plt.plot(ch0, label='0');plt.plot(ch1, label='1');plt.legend(loc=0)
plt.show()
ply.ylim(1800, 2100)
plt.ylim(1800, 2100)
plt.clf();plt.plot(ch0, label='y');plt.plot(ch1, label='x');plt.legend(loc=0)
xu1 = 3820;xu2=3870
yu1 = 4005;yu2=4055
xl1 = -8;xl2=0
yl1 = 241;yl2=332
ym1 = 1824;ym2=1965
xm1=2018;xm2=2048
xl1
xl2
xu1
(xu1-xl2)/2,xm1,xm2
(yu1-yl2)/2,ym1,ym2
def (b, t, ml, mu):
    deadzone = mu-ml
def (b, t, ml, mu):
    deadzone = mu-ml
def f(b, t, ml, mu):
    deadzone = mu-ml
    mid = ml + deadzone/2
    urange = t-mid
    lrange = mid-b
    if urange > lrange:
        r  = lrange
    else:
        r = urange
    return  mid, mid-r, mid+r, deadzone
    
xl1,xl2
xl1,xl2,xu1,xu2
f(xl2,xu1, xm1, xm2)
f(yl2,yu1, ym1, ym2)
