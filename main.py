from multiprocessing import Process, Queue
import os
import argparse
# Local imports
from data_collection.collect_stream import collect_stream
from data_collection.collect_radio import collect_radio
from data_collection.data_utils import monitor_song_name, get_song_name

def main(station='classical', dest='../../../../../../home/jastern33/audio_data', rate=44100, duration=60, break_on_song=False):
    """Records music of a certain type simultaneously from an internet streaming service
    and over the radio.
    Args:
        station (str): the type of music to record
        dest (str): the destination to store the recorded audio
        rate (int): the sample rate at which to record
        duration (int): the maximum song length in minutes
        break_on_song (bool): whether to break on song changes
    """
    if not os.path.exists(dest):
        os.makedirs(dest)

    song_name = get_song_name(station)
    while True:
        # Define Queue objects to pass messages to child processes
        q1 = Queue()
        q2 = Queue()
        # Define worker processes
        p1 = Process(target=collect_radio, args=(q1, song_name, station, dest, rate))
        p2 = Process(target=collect_stream, args=(q2, song_name, station, dest))
        try:
            # Start worker processes
            p1.start()
            p2.start()
            # Wait for a new song name
            song_name = monitor_song_name(station, duration, break_on_song)
            print("New song name:", song_name)
        finally:
            # Signal to the processes to quit
            q1.put(True)
            q2.put(True)
            p1.join()
            p2.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--station', required=False, type=str, default='classical', 
                        help='The type of station to record.',
                        choices=['classical', 'rock', 'country', 'talk'])
    parser.add_argument('-d', '--dest', required=False, type=str, default='../../../../../../home/jastern33/audio_data', 
                        help='The path for the recorded audio')
    parser.add_argument('-r', '--rate', required=False, type=int, default=44100, 
                        help='The sample rate for the recorded audio')
    parser.add_argument('--duration', required=False, type=float, default=30, 
                        help='The max song duration (in minutes)')
    parser.add_argument('--break_on_song', required=False, type=int, default=False, 
                        help='Whether to break on song changes (may be problematic if radio and stream are out of sync).')
    

    args = parser.parse_args()

    main(args.station,
        args.dest,
        args.rate,
        args.duration,
        args.break_on_song)