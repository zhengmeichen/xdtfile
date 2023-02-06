import h5py
import sys
import glob
import numpy as np
import matplotlib
import numpy
from PIL import Image
import os
SYSROOT = os.getenv('SYSTEM_ROOT', '.')
try:
    matplotlib.rc_file(SYSROOT + '/stweb/xlib/matplotlibrc')
except:
    matplotlib.use('Agg')
    traceback.print_exc()
from matplotlib import cm, dates, colors, pyplot as plt, ticker

datetime = sys.argv[1]
kind = sys.argv[2]
filelist = sorted(glob.glob(r'/FY3E/SEM/1A/%sOBC/2022/%s/*.HDF'%(kind,datetime)))
dict={}
for filename in filelist:
    print(filename)
    with h5py.File(filename,'r') as f:
        for k in f['Data'].keys():
            data = f['/Data/'+k][:]
            dims = data.ndim
            if dims==2:
                for i in range(data.shape[1]):
                    if k+str(i) not in dict.keys():
                        dict[k+str(i)]=data[:,i]
                    else:
                        dict[k + str(i)]=np.concatenate([dict[k+ str(i)],data[:,i]])
            elif dims==3:
                for i in range(data.shape[2]):
                    if k+str(i) not in dict.keys():
                        dict[k+str(i)]=data[:,:,i]
                    else:
                        dict[k + str(i)]=np.concatenate([dict[k+ str(i)],data[:,:,i]])
            else:
                if k not in dict.keys():
                    dict[k] = data[:]
                else:
                    dict[k] = np.concatenate([dict[k],data[:]])

for key,value in dict.items():
    print(key,len(value))
    plt.figure()
    plt.cla()
    plt.subplot(211)
    plt.plot(value,'-b.')
    plt.plot([np.mean(value)]*len(value),'r--')
    # plt.plot([-3*np.std(value)]*len(value),'r--')
    # plt.plot([3*np.std(value)]*len(value),'r--')
    plt.grid()
    plt.subplot(212)
    plt.plot(value-np.mean(value),'-b.')
    plt.plot([-3*np.std(value)]*len(value),'r--')
    plt.plot([3*np.std(value)]*len(value),'r--')
    plt.savefig('/STSS/FY3E_STSS/dev/AIWarning/PIC/'+key+'.png')