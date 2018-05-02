ifneq ($(KERNELRELEASE),)
	# call from kernel build system
	lifo-objs := main.o
	obj-m   := sunxi-debug-backdoor.o
else
	KERNELDIR ?= /lib/modules/$(shell uname -r)/build
	PWD       := $(shell pwd)
modules:
	echo $(MAKE) -C $(KERNELDIR) M=$(PWD) LDDINC=$(PWD)/../include modules
	$(MAKE) -C $(KERNELDIR) M=$(PWD) LDDINC=$(PWD)/../include modules
endif

clean:  
	rm -rf *.o *~ core .depend *.mod.o .*.cmd *.ko *.mod.c .tmp_versions *.markers *.symvers modules.order

depend .depend dep:
	$(CC) $(CFLAGS) -M *.c > .depend

ifeq (.depend,$(wildcard .depend))
	include .depend
endif
