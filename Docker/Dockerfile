FROM lofaruser/imaging-pipeline:latest

RUN apt-get update -y && apt-get upgrade -y && apt-get dist-upgrade -y

RUN apt-get install -qqy x11-apps -y
RUN apt install libaio1 libaio-dev
RUN apt install python3-matplotlib -y
RUN apt install python3-pyqt5 -y  
RUN apt install pyqt5-dev-tools -y
RUN apt install qttools5-dev-tools -y
RUN apt install python3-pip -y
RUN apt remove python2.7
RUN rm -rfv /usr/lib/python2.7
RUN apt install python3.6
RUN pip3 install seaborn coloredlogs configparser pyqt5==5.14

RUN wget https://lta.lofar.eu/software/lofar_lta-2.7.1.tar.gz
RUN tar -xzf /lofar_lta-2.7.1.tar.gz  -C / 
RUN cd /lofar_lta-2.7.1/ && python3  setup.py install_oracle && python3  setup.py install && python2 setup.py install_oracle && python2 setup.py install
RUN echo "LD_LIBRARY_PATH=/usr/lib/instantclient_11_2" >> /opt/lofarsoft/lofarinit.sh




