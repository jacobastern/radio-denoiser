from rtlsdr import RtlSdr
from contextlib import closing
from scipy import signal
from scipy.fftpack import fftshift
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

if __name__ == "__main__":

    #we use a context manager that automatically calls .close() on sdr
    #whether the code block finishes successfully or an error occurs
    #initializing a RtlSdr instance automatically calls open()
    with closing(RtlSdr()) as sdr:  
        sdr.sample_rate = sample_rate = 2400000
        sdr.center_freq = 97.5e6
        # sdr.gain = 20
        iq_samples = sdr.read_samples(3*sample_rate)

        # Intermediate downsample rate
        sample_rate_fm = 240000
        # Decimate (see https://en.wikipedia.org/wiki/Downsampling_(signal_processing))
        iq_comercial = signal.decimate(iq_samples, sample_rate//sample_rate_fm)
        angle_comercial = np.unwrap(np.angle(iq_comercial))
        demodulated_comercial = np.diff(angle_comercial)
        audio_rate = 44100
        audio_comercial = signal.decimate(demodulated_comercial, \
            sample_rate_fm//audio_rate, zero_phase=True)
        audio_comercial = np.int16(1e4*audio_comercial)
        wavfile.write("comercial_demodulated.wav", rate=audio_rate, data=audio_comercial)

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