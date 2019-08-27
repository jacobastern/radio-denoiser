import requests
from datetime import datetime
import os
import subprocess
from queue import Empty as QueueEmpty
# Local imports
from .data_utils import get_file_path#, get_url, get_metadata

def collect_stream(parent_queue, url, stream_format='.aac', genre='rock', rate=44100, dest='../data'):
    """Records an online radio stream from the given station until it receives a quit signal from
    its parent process
    Args:
        parent_queue (multiprocessing.Queue): a queue for receiving messages from the parent process
        url (str): the url to collect streamed audio
        stream_format (str): the format of the streamed audio
        genre (str): the genre of radio station to tune to
        dest (str): the destination for the song files
        rate (int): the rate at which to record samples
    """
    orig_file_path = get_file_path(genre, dest, audio_type='stream', ending=stream_format)
    wav_file_path = get_file_path(genre, dest, audio_type='stream', ending='.wav')
    
    # Get a Request object connected to the streaming url
    r = requests.get(url, stream=True)

    try:
        with open(orig_file_path, 'wb') as f:
            for block in r.iter_content(1024):
                f.write(block)
                # Break out if producer says quit
                try:
                    parent_queue.get(timeout=0)
                    break
                except QueueEmpty:
                    pass
    finally:
        # Convert the original file to .wav file
        bash_command = 'ffmpeg -loglevel panic -i {} -ar {} -sample_fmt s16 -ac 1 {}'.format(orig_file_path, rate, wav_file_path)
        subprocess.run(bash_command.split())
        # Remove the original file
        bash_command = 'rm {}'.format(orig_file_path)
        subprocess.run(bash_command.split())