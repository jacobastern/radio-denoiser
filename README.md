# Radio Denoiser

This package is for experiments attempting to remove static from a radio signal received over the airwaves.

It has two parts: data collection, and denoising. For data collection, this package provides scripts to collect your own dataset.

### Requirements

[Docker](https://docs.docker.com/install/)

An RTL2832U [radio dongle](https://www.amazon.com/RTL-SDR-Blog-RTL2832U-Software-Defined/dp/B011HVUEME/ref=pd_bxgy_23_img_3/132-0436988-4436743?_encoding=UTF8&pd_rd_i=B011HVUEME&pd_rd_r=e374f032-114a-44fd-8935-ae9b16d30516&pd_rd_w=6uxQr&pd_rd_wg=v2f8y&pf_rd_p=a2006322-0bc0-4db9-a08e-d168c18ce6f0&pf_rd_r=B5MF99MD4PY6CDS6WXK5&psc=1&refRID=B5MF99MD4PY6CDS6WXK5)

### Usage: Data Collection
1. Clone the repo:
```bash
git clone https://github.com/jastern33/radio-denoiser.git
cd radio-denoiser
```
2. Build the docker image: 
```bash
cd docker
docker build -t deep-learning-pytorch -f Dockerfile . --rm
```
3. Run a docker container based on that image: 
```bash
cd ..
nvidia-docker run -it --name data-collection --rm -v $(pwd):/code -v path/to/data:data deep-learning-pytorch
```
4. Pick an radio statio to record.
    - Find a local (FM) radio station that is also streamed over the internet.
    - Obtain the streaming url as described in [this video](https://www.youtube.com/watch?v=J3Es00azAT4).

5. Run:
```bash
python3 data_collect_main.py --frequency <radio_freq> --url <streaming_url> --format <streamed_format>`
```
For example,
```bash
python3 data_collect_main.py --frequency 89.1 --url http://cdn.byub.org/classical89/classical89_mp3 --format .mp3`
```
A Note:

`data_collect_main.py` collects streamed and broadcast radio in its native format and converts it to signed-16-bit-little-endian, 44.1kHz, single-channel `.wav` files. If it doesn't work with the default `--format`, which is `.aac`, try `.mp3`.

### Usage: Radio Denoising
Not yet implemented

### TODO:
- Adapt [Wave U-Net](https://github.com/f90/Wave-U-Net) to use for denoising.
- Implement [Complex U-Net](https://openreview.net/forum?id=SkeRTsAcYm) using https://github.com/litcoderr/ComplexCNN as a building block
