import h5py
import sys
import glob
import numpy as np
datetime = sys.argv[1]
# kind = sys.argv[2]
# filelist = sorted(glob.glob(r'/FY3E/SEM/1A/%sOBC/2022/%s/*.HDF'%(kind,datetime)))
filelist = sorted(glob.glob('/FY3E/HIRAS/1A/OBC/2022/%s/*.HDF'%(datetime)))
dict={}
for filename in filelist[:19]:
    print(filename)
    with h5py.File(filename,'r') as f:
        for k in f['Tele'].keys():
            data = f['/Tele/'+k][:]
            dims = data.ndim
            if dims==2:
                for i in range(data.shape[1]):
                    if k+str(i) not in dict.keys():
                        dict[k+str(i)]=np.unique(data[:,i])
                    else:
                        dict[k + str(i)]=np.concatenate([dict[k+ str(i)],np.unique(data[:,i])])
            elif dims==3:
                for i in range(data.shape[2]):
                    if k+str(i) not in dict.keys():
                        dict[k+str(i)]=np.unique(data[:,:,i])
                    else:
                        dict[k + str(i)]=np.concatenate([dict[k+ str(i)],np.unique(data[:,:,i])])
            else:
                if k not in dict.keys():
                    dict[k] = np.unique(data[:])
                else:
                    dict[k] = np.concatenate([dict[k],np.unique(data[:])])

for key,value in dict.items():
    print(key,len(value))



