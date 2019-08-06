import multiprocessing
from collect_stream import collect_stream
from collect_radio import collect_radio
from monitor_song import monitor_song_name, get_song_name



def main(dest='rock', root='../../work/data/'):
    
    song_name = get_song_name(url)
    while True:
        start_threads({
        collect_radio(song_name, dest, root)
        collect_stream(song_name, dest, root)
        })
        song_name = monitor_song_name(url)
        join_threads({})


if __name__ == "__main__":
    main()