import re
from urllib import request
import struct
import time
import re
import unicodedata
from datetime import datetime
import os

def get_url(dest):
    """Gets the streaming url for a type of music. This url can be obtained from the
     .pls playlist file available from many streaming websites. Make sure to get the 
     mp3 url, not the aac url. If you can't find the url, see this tutorial on how to 
     track it down: https://www.youtube.com/watch?v=J3Es00azAT4"""

    if dest == 'classical':
        # 89.5 KBYU Classical
        url = 'http://cdn.byub.org/classical89/classical89_mp3'

    elif dest == 'country':
        # 97.7 The Wolf
        url = 'https://ice9.securenetsystems.net/KWUT?&playSessionID=14183F23-AD77-917F-BDD7025E827C38CD'

    elif dest == 'talk':
        # 102.7 KSL News Radio
        url = 'http://14033.live.streamtheworld.com:3690/KSLAM_SC?DIST=TuneIn&TGT=TuneIn&maxServers=2&ua=RadioTime&ttag=RadioTime'

    elif dest == 'rock':
        # 106.7 KAAZ-FM
        url = 'http://c3icyelb.prod.playlists.ihrhls.com/2397_icy'
    
    return url

def get_file_path(song_name, dest, root, audio_type, ending):

    today = datetime.today()
    year, month, day = str(today.year), str(today.month), str(today.day)

    file_path = os.path.join(root, '_'.join([year, month, day, dest, audio_type, song_name]))

    if os.path.exists(file_path + ending):

        i = 0
        while os.path.exists(file_path + str(i).zfill(3) + ending):
            i += 1

        return file_path + str(i).zfill(3) + ending

    return file_path + ending

def get_song_name(dest):
    """Gets the name of the song currently being streamed from a website. Adapted from:
    https://stackoverflow.com/questions/35102278/python-3-get-song-name-from-internet-radio-stream
    Args:
        dest (str): the category of music ('rock', 'classical', 'talk', 'country')
    """
    url = get_url(dest)
    encoding = 'iso-8859-1' # default: iso-8859-1 for mp3 and utf-8 for ogg streams
    req = request.Request(url, headers={'Icy-MetaData': 1})  # request metadata
    response = request.urlopen(req)
    metaint = int(response.headers['icy-metaint'])
    for _ in range(10): # title may be empty initially, try several times
        response.read(metaint)  # skip to metadata
        metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
        metadata = response.read(metadata_length).rstrip(b'\0')
        # print(metadata)
        if dest == 'talk':
            return ""
        elif dest == 'rock':
            song_title = re.search('(?<={}).*?(?={})'.format('StreamTitle', 'text'), metadata)
            artist = artist.group(1)
            song_title = re.search('(?<={}).*?(?={})'.format('text', 'song_spot'), metadata)
            song_title = song_title.group(1)
            print(artist, song_title)
        else:
            # extract title from the metadata
            m = re.search(br"StreamTitle='([^']*)';", metadata)
            title = m.group(1)
            if m:
                if title:
                    return convert_to_filestring(title.decode(encoding, errors='ignore'))

def monitor_song_name(dest):
    """Monitors the song name currently streamed at a given url, returns when the song changes"""
    song = get_song_name(dest)
    start_time = time.time()
    while True:
        # new_song = get_song_name(dest)
        # # Start new track at song change or timeout (20 min)
        # if new_song != song or (time.time() - start_time) > (60*.3):
        #     return new_song
        time.sleep(10000)

def convert_to_filestring(name):
    """
    Normalizes string, converting non-alphanumeric characters to underscores
    Copied from: https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    """
    name = "".join(x for x in name if x.isalnum())
    return name