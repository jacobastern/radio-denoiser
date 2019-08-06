import requests
from datetime import datetime
import os

def get_stream_info(song_name, dest, root):

    today = datetime.today()
    year, month, day = str(today.year), str(today.month), str(today.day)

    # This can be obtained from the .pls playlist file available from many streaming websites. Make sure
    # to get the mp3 url, not the aac url. If you can't find the url, see this tutorial on how to track
    # it down: https://www.youtube.com/watch?v=J3Es00azAT4
    if dest == 'classical':
        # 89.5 KBYU Classical
        url = 'http://cdn.byub.org/classical89/classical89_mp3'
        file_path = os.path.join(root, year + month + day + '_' + dest + '_' + song_name + '_stream' + '.mp3')

    elif dest == 'country':
        # 97.7 The Wolf
        url = 'https://ice9.securenetsystems.net/KWUT?&playSessionID=14183F23-AD77-917F-BDD7025E827C38CD'
        file_path = os.path.join(root, year + month + day + '_' + dest + '_' + song_name + '_stream' + '.mp3')

    elif dest == 'talk':
        # 102.7 KSL News Radio
        url = 'http://14033.live.streamtheworld.com:3690/KSLAM_SC?DIST=TuneIn&TGT=TuneIn&maxServers=2&ua=RadioTime&ttag=RadioTime'
        file_path = os.path.join(root, year + month + day + '_' + dest + '_' + song_name + '_stream' + '.mp3')

    elif dest == 'rock':
        # 106.7 KAAZ-FM
        url = 'http://c3icyelb.prod.playlists.ihrhls.com/2397_icy'
        file_path = os.path.join(root, year + month + day + '_' + dest + '_' + song_name + '_stream' + '.mp3')
    
    return url, file_path

def collect_stream(song_name, dest='rock', root='../../work/data'):

    url, file_path = get_stream_info(song_name, dest, root)

    r = requests.get(url, stream=True)

    with open(file_path, 'wb') as f:
        print("File opened")
        try:
            for block in r.iter_content(1024):
                print("Received a block!")
                f.write(block)
        except KeyboardInterrupt:
            pass