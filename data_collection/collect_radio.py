import os
import subprocess
import time
from queue import Empty as QueueEmpty
from .data_utils import get_file_path

def collect_radio(parent_queue, freq, genre='rock', rate=44100, dest='work/data'):
    """Records a radio signal at the given station until it receives a quit signal from
    its parent process
    Args:
        parent_queue (multiprocessing.Queue): a queue for receiving messages from the parent process
        song_name (str): the name of the song
        station (str): the type of radio station to tune to
        dest (str): the destination for the song files
        rate (int): the rate at which to record samples
    """

    raw_file_path = get_file_path(genre, dest, audio_type='radio', ending='.raw')
    wav_file_path = get_file_path(genre, dest, audio_type='radio', ending='.wav')

    rate = str(rate / 1000) + 'k'
    
    # -s Original sample rate: 170k
    # -r Resample to: 44.1k
    # -f Tune to frequency: 89.1M
    # -l 0 Disable squelch
    bash_command = 'rtl_fm -f {} -l 0 -g 40.2 -s 170k -r {} {}'.format(freq, rate, raw_file_path)

    proc = subprocess.Popen(bash_command.split())
    try:
        while True:
            # Break out if producer says quit
            try:
                time.sleep(.5)
                parent_queue.get(timeout=0)
                break

            except QueueEmpty:
                pass
    finally:
        proc.terminate()
        # Give sufficient time to disconnect from the device
        time.sleep(1)
        # Save the .raw file as a .wav file by adding a header
        bash_command = 'ffmpeg -loglevel panic -ar {} -f s16le -ac 1 -i {} {}'.format(rate, raw_file_path, wav_file_path)
        subprocess.run(bash_command.split())
        # Remove the original file
        bash_command = 'rm {}'.format(raw_file_path)
        subprocess.run(bash_command.split())
            
