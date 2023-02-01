import numpy as np
import matplotlib.pyplot as plt

aa = np.array([1, 2, 3, 4, 5, 6])
bb = np.array([2, 32, 23, 12, np.nan, 22])
xx = np.isnan(bb)
bb = bb[~xx]
aa = aa[~xx]

cc = np.array([11, 22, 33, 44, 66])

x = plt.plot(aa, bb,linestyle='-.')
y = plt.plot(aa, cc)
# plt.legend([x, y], ['xx', 'yy'], loc='upper left')
plt.legend(["BJ", "SH"])
plt.savefig('xxx.png')
plt.show()
