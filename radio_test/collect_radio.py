from datetime import datetime
import os
import rtlsdr
from rtlsdr.rtlsdr import RtlSdr
from queue import Empty as QueueEmpty
from scipy import signal
from scipy.io import wavfile
import numpy as np
from contextlib import closing
from .data_utils import get_file_path

def tune_to(dest, sample_rate=2400000, gain=0):
    """Tunes to the station at the given frequency, returns RtlSdr object tuned to that station
    Args:
        dest (str): the destination ('rock', 'classical', 'country', 'talk')
        sample_rate (int): defaults to 926100, the smallest integer multiple of 44100 in 2205000
            the valid sample range. Valid sample range: [225001, 300000] U [900001, 3200000]
    """
    if dest == 'classical':
        # 89.5 KBYU Classical
        # Note: the radio transmission is about 3 minutes ahead of the online stream
        freq = '89.5'
    elif dest == 'country':
        # 97.7 The Wolf
        freq = '97.7'
    elif dest == 'talk':
        # 102.7 KSL News Radio
        freq = '97.5'
    elif dest == 'rock':
        # 106.7 KAAZ-FM
        freq = '106.7'
    else:
        raise TypeError("Invalid Destination")

    try:
        sdr = RtlSdr()
    except OSError as e:
        print(e)
        print("If the error code is '-6', make sure that no other program is trying to access \
            this device.")
        raise
    sdr.sample_rate = sample_rate
    sdr.sample_rate = int(sample_rate)
    sdr.center_freq = float(freq) * 1e6
    sdr.gain = gain

    return sdr


def collect_radio(parent_queue, song_name, dest='rock', root='work/data', audio_rate=44100):

    # sdr = tune_to(dest)
    # sdr_sample_rate = int(sdr.sample_rate)
    file_path = get_file_path(song_name, dest, root, audio_type='radio', ending='.wav')

    sample_arr = np.array([])

    with closing(RtlSdr()) as sdr:  
        sdr.sample_rate = 10*5*audio_rate
        sample_rate_fm = 5*audio_rate
        sdr.center_freq = 97.5e6
        while True:
            # source: http://ajoo.blog/tag/python.html
            # Read 1s of audio
            # sdr.gain = 20
            iq_samples = sdr.read_samples(1024*8)
            # Intermediate downsample rate
            # Decimate (see https://en.wikipedia.org/wiki/Downsampling_(signal_processing))
            iq_samples = signal.decimate(iq_samples, int(sdr.sample_rate)//sample_rate_fm)
            angle_samples = np.unwrap(np.angle(iq_samples))
            demodulated_samples = np.diff(angle_samples)
            audio_samples = signal.decimate(demodulated_samples, \
                sample_rate_fm//audio_rate, zero_phase=True)
            sample_arr = np.append(sample_arr, np.int16(1e4*audio_samples))
            print(len(sample_arr))
            # Break out if producer says quit
            try:
                parent_queue.get(timeout=0)
                wavfile.write(file_path, rate=audio_rate, data=sample_arr)
                return
            except QueueEmpty:
                pass
    # with open(file_path, 'wb') as f:
    #     print("File opened") 
    #     # Define a callback to pass into the stream reader
    #     def samples_callback(samples):
    #         print("Received a block!")
    #         f.write(samples)
    #     try:
    #         while True:
    #             sdr.read_samples_async(samples_callback, num_samples=1024)
    #     except KeyboardInterrupt:
    #         pass


    # Working:
    #     file_path = get_file_path(song_name, dest, root, audio_type='radio', ending='.wav')

    # sample_arr = np.array([])

    # with closing(RtlSdr()) as sdr:  
    #     while True:
    #         # source: http://ajoo.blog/tag/python.html
    #         # Read 1s of audio
    #         sdr.sample_rate = sample_rate = 2400000
    #         sdr.center_freq = 97.5e6
    #         # sdr.gain = 20
    #         iq_samples = sdr.read_samples(3*sample_rate)
    #         # Intermediate downsample rate
    #         sample_rate_fm = 240000
    #         # Decimate (see https://en.wikipedia.org/wiki/Downsampling_(signal_processing))
    #         iq_samples = signal.decimate(iq_samples, int(sdr.sample_rate)//sample_rate_fm)
    #         angle_samples = np.unwrap(np.angle(iq_samples))
    #         demodulated_samples = np.diff(angle_samples)
    #         audio_rate = 44100
    #         audio_samples = signal.decimate(demodulated_samples, \
    #             sample_rate_fm//audio_rate, zero_phase=True)
    #         # print(audio_samples)
    #         sample_arr = np.append(sample_arr, np.int16(1e4*audio_samples))

    #         # # print("block received! Type: ", type(samples))
    #         # decimated_iq_samples = decimate(iq_samples, int(sdr.sample_rate)//audio_rate)
    #         # angle_samples = np.unwrap(np.angle(decimated_iq_samples))
    #         # demodulated_samples = np.diff(angle_samples)
    #         # demodulated_samples = np.int16(1e4*demodulated_samples)
    #         # wavfile.write(file_path, rate=audio_rate, data=demodulated_samples)
    #         # # wavfile.write(file_path, rate=(2.4e6 / 50), data=decimate(decimate(samples, 10), 5)).real() # 2.4e6 / 50 = 48k
    #         # Break out if producer says quit
    #         try:
    #             parent_queue.get(timeout=0)
    #             wavfile.write(file_path, rate=audio_rate, data=sample_arr)
    #             return
    #         except QueueEmpty:
    #             pass