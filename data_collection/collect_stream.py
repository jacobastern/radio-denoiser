import requests
from datetime import datetime
import os
from queue import Empty as QueueEmpty
from .data_utils import get_url, get_file_path

def collect_stream(parent_queue, song_name, dest='rock', root='work/data', process_stop=False):

    url = get_url(dest)
    file_path = get_file_path(song_name, dest, root, audio_type='stream', ending='.mp3')

    r = requests.get(url, stream=True)

    with open(file_path, 'wb') as f:
        for block in r.iter_content(1024):
            # print("Received a block! Type: ", type(block))
            f.write(block)
            # Break out if producer says quit
            try:
                parent_queue.get(timeout=0)
                return
            except QueueEmpty:
                pass