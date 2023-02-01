# make file
all:
	gcc -fno-strict-aliasing -g -O2 -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC \
		`python3-config --includes` \
		-L`python -c 'import numpy;print (numpy.get_include())'` \
		-c _nmqc.c -o _nmqc.o
	gcc -pthread -shared _nmqc.o -o _nmqc.so
	rm _nmqc.o
clean:
	rm _nmqc.so