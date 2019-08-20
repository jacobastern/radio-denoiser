#FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04
FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

ARG DEBIAN_FRONTEND=noninteractive

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# install build tools & python
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libjpeg-dev \
    libpng-dev \
    build-essential \
    cmake \
    curl \
    g++ \
    git \
    graphicsmagick \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libfreetype6-dev \
    libgraphicsmagick1-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libpng-dev \
    librtlsdr-dev \
    libswscale-dev \
    libzmq3-dev \
    pkg-config \
    protobuf-compiler \
    python3 \
    python3-dev \
    python3-pip \
    python3-tk \
    python3-lxml \
    python3-setuptools \
    rsync \
    software-properties-common \
    unzip \
    wget \
    vim \
    zip

# install cleanup
RUN apt-get -qq update && apt-get -qq clean \
    && rm -rf /var/lib/apt/lists/*

# update python installers
RUN pip3 install pip --upgrade

# install python dependencies
RUN pip3 --no-cache-dir install \
    argparse \
    opencv-python \
    sklearn \
    cython \
    ipykernel \
    jupyter \
    matplotlib \
    numpy \
    seaborn \
    pprint \
    requests \
    scipy \
    setuptools \    
    xgboost \
    h5py \
    torch==1.1.0 -f https://download.pytorch.org/whl/cu100/stable \
    && python3 -m ipykernel.kernelspec

ENTRYPOINT ["/bin/bash"]



