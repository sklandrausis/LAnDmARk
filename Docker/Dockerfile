FROM lofaruser/imaging-pipeline:latest

RUN apt-get update -y && apt install apt-utils -y -&& apt-get upgrade -y && apt-get dist-upgrade -y

RUN apt-get install -qqy x11-apps -y
RUN apt install libaio1 libaio-dev
RUN apt install python3-matplotlib -y
RUN apt install python3-pyqt5 -y
RUN apt install pyqt5-dev-tools -y
RUN apt install qttools5-dev-tools -y
RUN apt install python3-pip -y
RUN apt install screen -y

RUN pip3 install seaborn coloredlogs configparser pyqt5==5.14

RUN wget https://lta.lofar.eu/software/lofar_lta-2.7.1.tar.gz
RUN tar -xzf /lofar_lta-2.7.1.tar.gz  -C / 
RUN cd /lofar_lta-2.7.1/ && python3  setup.py install_oracle && python3  setup.py install && python2 setup.py install_oracle && python2 setup.py install
RUN echo "export LD_LIBRARY_PATH=/usr/lib/instantclient_11_2" >> /opt/lofarsoft/lofarinit.sh
RUN echo "export PYTHONPATH=''" >> /opt/lofarsoft/lofarinit.sh
RUN cp -rfv /opt/lofarsoft/lib/python2.7/site-packages/* /usr/local/lib/python2.7/dist-packages/

RUN git clone https://github.com/lofar-astron/LofarStMan.git /LofarStMan
RUN mkdir /LofarStMan/build
RUN ln -s /opt/lofarsoft/include/casacore/* /usr/include/
RUN ln -s /opt/lofarsoft/lib/*so* /usr/lib/
RUN ln -s /opt/lofarsoft/include/casacore/ /usr/include/casacore
RUN cd /LofarStMan/build && cmake ../ && make && make install
RUN ln -s  /usr/local/lib/liblofarstman.so /opt/lofarsoft/lib/liblofarstman.so



