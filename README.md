# gnuradio-docker
Gnuradio Docker with AISTX, ADSB, HACKRF, SOAPY, &amp; OSMOCOM


Setting Gnuradio-docker


setting docker:

    1. make sure docker is already install and hve permission if not: do this:

sudo usermod -a -G docker $USER

    2. then reboot

    3. copy image file to directory
    4. In terminal go to diredtory part
	cd totem
	totem$ ls
		gnuradio-totem  gnuradio-totem.tar.gz  totem-fw-env  totem-fw-env.tar.gz
	totem$ docker load -i gnuradio-totem.tar.gz 

    5. wait until the process is done

    6. move to the path which there is gnuradio-docker.sh inside 

    7. make sure file in gnuradio-totem has gnuradio-docker.sh

	totem/gnuradio-totem$ ./gnuradio-docker.sh

Build a new docker using dockerfile and add Packages

	1. add syntax in dockerfile
	2. build it
		docker build -f Dockerfile.mau -t gnuradio-totem:mau .
	3. edit ./gnuradio.sh
		mention the new image in the last sentence with the new tag
	4. run with the new sh
