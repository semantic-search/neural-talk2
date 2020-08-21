FROM nagadomi/torch7:latest
RUN luarocks install nn
RUN luarocks install image
RUN luarocks install lua-cjson
RUN luarocks install https://raw.githubusercontent.com/jcjohnson/torch-rnn/master/torch-rnn-scm-1.rockspec
RUN luarocks install nngraph
RUN apt-get install -y libprotobuf-dev protobuf-compiler
RUN luarocks install loadcaffe
RUN apt-get install -y libhdf5-serial-dev hdf5-tools
RUN git clone https://github.com/anibali/torch-hdf5.git
RUN cd torch-hdf5 && git checkout hdf5-1.10 && luarocks make hdf5-0-0.rockspec
RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get install wget

RUN apt-get purge -y cmake
RUN git clone https://github.com/Kitware/CMake.git
RUN apt-get install libssl-dev
RUN cd CMake && ./bootstrap; make; sudo make install

RUN apt-get install -y python3-pip
RUN pip3 install install fastapi[all]
COPY main.py .
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN git clone https://github.com/karpathy/neuraltalk2.git
WORKDIR neuraltalk2
RUN wget http://cs.stanford.edu/people/karpathy/neuraltalk2/checkpoint_v1.zip