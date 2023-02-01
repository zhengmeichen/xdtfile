
#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

// Forward function declaration.
static PyObject *NDMQC(PyObject *self, PyObject *args); 

// Boilerplate: method list.
static PyMethodDef methods[] = {
  { "NDMQC", NDMQC, METH_VARARGS, "C-API Function (BBOY)\n \
ndmqc.NDMQC \
usage: \n \
  NDMQC(scan,size,kk,n,data,qc)  \n \
data type: \n \
  npy_int64/pyint    : scan - scanline for data; size - total size for data; kk (ndmqc - kk) \n \
  npy_float64/pyfloat: n (ndmqc - n) \n \
  npy_ndarray (c format) \n \
    dtype = npy_float64/pyfloat:  data \n \
    dtype = npy_int64/pyint    :  qc   (byref)\n \
return None \n "},
  { NULL, NULL, 0, NULL } /* Sentinel */
};

// Boilerplate: Module initialization.
PyMODINIT_FUNC initndmqc(void) {
  (void) Py_InitModule("ndmqc", methods);
  import_array();
}
/**

*/
npy_float64 qmed(npy_float64* pData,int left,int right, int nd) {  // modifrom qsort
    //printf("\ndo-  >left=%d,right=%d,nd2=%d, median: %f" ,left,right,nd,pData[nd]);
    npy_float64 middle,iTemp;
    int i,j;
    i = left;
    j = right;
    middle = pData[nd];//pData[(left+right)/2]; //求中间值
    do{
        while((pData[i]<middle) && (i<right))//从左扫描大于中值的数
                       i++;
        while((pData[j]>middle) && (j>left))//从右扫描大于中值的数
                       j--;
        if(i<=j)//找到了一对值
            {//交换
                iTemp = pData[i];
                pData[i] = pData[j];
                pData[j] = iTemp;
                i++;
                j--;
            }
    }while(i<=j);
    //如果两边扫描的下标交错，就停止（完成一次）//当左边部分有值(left<j)，递归左半边
    //printf("@ left:%d,right:%d,i=%d,j=%d, nd=%d::mid=%d,r-l%d\n",left,right,i,j,nd,middle,right-left);
    //if(left<j )   run(pData,left,j);
    //if(right>i)   run(pData,i,right);
    if (nd<=j)
        return qmed(pData,left,j,nd);
    else if  (nd>=i)
        return qmed(pData,i,right,nd);
    else{
    //	printf("\n->left=%d,right=%d,nd2=%d, median: %f" ,left,right,nd,pData[nd]);
	return pData[nd];
	}
}

npy_float64 median(npy_float64 *a,int len){
	npy_float64 data[len];
	int right;
	for (right=0;right<len;right++) data[right]=a[right];
	right--;
	if (right<0) return 0;
	//printf("\n len %i, right %i",len,right);
	return qmed(data,0,right,len/2);
}

/*****************************************************************************
 * NDMQC                                                                     *
 *****************************************************************************/

void ndmqc_fun(npy_float64 *arr,npy_int64 *qc ,npy_int64 kk ,npy_float64 n,npy_int64 scan)
{		
	int i,j;
	//npy_float64 data[scan];// data
	npy_float64 *data=(npy_float64*)malloc(sizeof(npy_float64)*scan);
	npy_float64 div;       // chk point    
	//prepare data
    //	printf("\ndata in ndmqc fun\n");
	int dts=0;
	j=1;
	for(i=0;i<scan;i++){
    //		printf("    \033[%sm%8.2f %d\033[0m,%s",(qc[i]==0?"32":"31"),arr[i],qc[i],(j%10==0?"\n":"   "));j++;
		if(qc[i] == 0){
		data[dts]=arr[i];
		dts++;
		}}
	int  c[dts];   // de fen
	for(j=0;j<dts;j++)c[j]=0;
	for(j=0;j<kk;j++){i=(kk-j+1)/2;c[j]=i;c[dts-j-1]=i;}
        npy_float64 tmp[dts]; // cha biao
	dts--;
	for(i=0;i<kk;i++){
		for(j=0;j<dts-i;j++){
			tmp[j] = abs(data[j+i+1]-data[j]);
			//printf("\n%d - %d = %d",data[j+i+1] ,data[j] ,tmp[j] );
			}
		div = median(tmp,dts-i);		
		div = div * n;
		// printf("div=%2.2f, dts-i=%d ",div,dts-i);
		for(j=0;j<dts-i;j++){
			if (tmp[j]>div){
				c[j]++;
				c[j+i+1]++;
				    /*printf("\033[31m%.2f\033[0m,",tmp[j]);//*/
				}   // else printf("%.2f,",tmp[j]);
				}
		}

	int countqc = 0;	
	dts=0;
    //	printf("\nQC>>\n");
	for(i=0;i<scan;i++){
        //		if (i%10==0) printf("\n");
		if(qc[i]==0){
			if(c[dts]>kk){
				qc[i]=1;
				countqc++;
				// printf("    \033[31m%8.2f%2d\033[0m,   ",arr[i],qc[i]);
				}  //  else printf("    %8.2f%2d,   ",arr[i],qc[i]);//*/                       
			dts++;
			}   // else printf("    \033[32m%8.2f%2d\033[0m,  ",arr[i],qc[i]);	//*/
		}
    //	printf("\n");
	if ((countqc > 2*kk)& (scan-countqc>2*kk))	{
		ndmqc_fun(arr,qc,kk,n,scan);
		}

	free(data);
}

/*
void test(int *a,int *b){
	a=(int*)a;
	a[0]=2;
	b[0]=2;
	printf("\n in test %d,%d",a[0],b[0]);
}*/
/*****************************************************************************
 * NDMQC                                                                    *
 *****************************************************************************/
static PyObject *NDMQC(PyObject *self, PyObject *args) {
  // Declare variables. 
  npy_int64      scan, kk, size;
  npy_float64    n;
  PyArrayObject *py_data, *py_qc;
  npy_float64 *data;
  npy_int64  *qc;
  
  printf ("\033[33m -- C-API Function Used --\033[0m                                                \n");
  int z,i,j,k;
  // Parse arguments. 
  if (!PyArg_ParseTuple(args, "llldO!O!",
	&scan,
	&size,
	&kk,
	&n,
	&PyArray_Type, &py_data,
	&PyArray_Type, &py_qc)) {
    return NULL;
  }

    //  printf("scan:%d,size,%d; kk: %d, n %f\n",scan,size,kk,n);
  data = (npy_float64*)   PyArray_DATA(py_data);
  qc   = (npy_int64*)    PyArray_DATA(py_qc);
  npy_int64 tmpqc[scan];
  npy_float64 tmpdt[scan];
    //  int x,y;x=0;y=0;
  z=size/scan;
  for (i=0;i<z;i++){
    //     printf("\033[33m -[Cython debuginfo ]: inner cnl %d -----------------------------------\033[0m\n",i);x++;
     for(j=0;j<scan;j++){
       k =  j*z + i;
        //       printf("\033[%sm%-4d,%7.2f,%d;\033[0m %s",(qc[k]==0?"34":"31"),k,data[k],qc[k],(x%10==0?"\n":"  "));x++;
       tmpqc[j]=qc[k];
       tmpdt[j]=data[k];
     }
     ndmqc_fun(tmpdt,tmpqc,kk,n,scan);
        //     x=1;
     for(j=0;j<scan;j++){
       k =  j*z + i;
        //       printf("\033[%sm%-4d,%7.2f,%d;\033[0m %s",(tmpqc[j]==0?"34":"31"),k,tmpdt[j],tmpqc[j],(x%10==0?"\n":"  "));x++;
       qc[k]=tmpqc[j];
     }
  }
  Py_RETURN_NONE;
}
