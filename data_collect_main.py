from multiprocessing import Process, Queue
import os
import argparse
import time
# Local imports
from data_collection.collect_stream import collect_stream
from data_collection.collect_radio import collect_radio
# from data_collection.data_utils import monitor_song_name, get_song_name

def main(freq=None, url=None, stream_format='.aac', genre='classical', rate=44100, duration=30, dest='../data'):
    """Records music of a certain type simultaneously from an internet streaming service
    and over the radio.
    Args:
        freq (float): the FM radio frequency to record
        url (str): the url to collect streamed audio
        stream_format (str): the format of the streamed audio
        rate (int): the sample rate at which to record
        duration (int): the maximum song length in minutes
        dest (str): the destination to store the recorded audio
        station (str): the type of music to record
        break_on_song (bool): whether to break on song changes
    """
    if not os.path.exists(dest):
        os.makedirs(dest)

    while True:
        # Define Queue objects to pass messages to child processes
        q1 = Queue()
        q2 = Queue()
        # Define worker processes
        p1 = Process(target=collect_radio, args=(q1, freq, genre, rate, dest))
        p2 = Process(target=collect_stream, args=(q2, url, stream_format, genre, rate, dest))
        try:
            # Start worker processes
            p1.start()
            p2.start()
            # Record for specified duration
            time.sleep(duration * 60)
        finally:
            # Signal to the processes to quit
            q1.put(True)
            q2.put(True)
            p1.join()
            p2.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--freq', required=True, type=float,
                        help='The FM frequency to record.')
    parser.add_argument('-u', '--url', required=True, type=str,
                        help='The url for the streamed radio to record.')
    parser.add_argument('-s', '--stream_format', required=False, type=str, default='.aac', 
                        help='The audio format of the incoming streamed audio.')
    parser.add_argument('-g', '--genre', required=False, type=str, default='DefaultGenre', 
                        help='The genre of the radio station.')
    parser.add_argument('-r', '--rate', required=False, type=int, default=44100, 
                        help='The sample rate for the recorded audio')
    parser.add_argument('-d', '--duration', required=False, type=float, default=30, 
                        help='The max song duration (in minutes)')
    parser.add_argument('--dest', required=False, type=str, default='../data', 
                        help='The path for the recorded audio')
    

    args = parser.parse_args()

    main(args.freq,
        args.url,
        args.stream_format,
        args.genre,
        args.rate,
        args.duration,
        args.dest,)