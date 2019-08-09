from multiprocessing import Process, Queue
import os

from data_collection.collect_stream import collect_stream
# from data_collection.collect_radio import collect_radio
from data_collection.data_utils import monitor_song_name, get_song_name



def main(dest='classical', root='../../../../../../home/jastern33', audio_rate=44100):
    
    if not os.path.exists(root):
        os.makedirs(root)

    song_name = get_song_name(dest)
    while True:
        # Define Queue objects to pass messages to child processes
        # q1 = Queue()
        q2 = Queue()
        # Define worker processes
        # p1 = Process(target=collect_radio, args=(q1, song_name, dest, root, audio_rate))
        try:
            p2 = Process(target=collect_stream, args=(q2, song_name, dest, root))
            # Start worker processes
            # p1.start()
            p2.start()
            input("Recording {}. Press any key to exit.".format(dest))
            # Signal to the processes to quit
            # q1.put(True)
            q2.put(True)
            # p1.join()
            p2.join()
        except KeyboardInterrupt:
            raise


if __name__ == "__main__":
    main()



# Old Code

# Wait for a new song name
# song_name = monitor_song_name(dest)
# print("New song name")