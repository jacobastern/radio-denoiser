import re
from urllib import request
import struct
import time
import re
import unicodedata
from datetime import datetime
import os
from http.client import RemoteDisconnected
from urllib.error import HTTPError

def get_url(station):
    """Gets the streaming url for a type of music. This url can be obtained from the
    .pls playlist file available from many streaming websites. Make sure to get the 
    mp3 url, not the aac url. If you can't find the url, see this tutorial on how to 
    track it down: https://www.youtube.com/watch?v=J3Es00azAT4
    Args:
        station (str): the station to record audio from
    Returns:
        url (str): the streaming url
        ending (str): the type of file streamed from that url
    """

    if station == 'classical':
        # 89.5 KBYU Classical
        url = 'http://cdn.byub.org/classical89/classical89_mp3'
        ending = '.mp3'

    elif station == 'country':
        # 97.7 The Wolf
        url = 'https://ice9.securenetsystems.net/KWUT?&playSessionID=14183F23-AD77-917F-BDD7025E827C38CD'
        ending = '.aac'

    elif station == 'talk':
        # 102.7 KSL News Radio
        url = 'http://14033.live.streamtheworld.com:3690/KSLAM_SC?DIST=TuneIn&TGT=TuneIn&maxServers=2&ua=RadioTime&ttag=RadioTime'
        ending = '.mp3'

    elif station == 'rock':
        # 106.7 KAAZ-FM
        # raise NotImplementedError("No metadata for rock mp3 stream")
        url = 'http://c3icyelb.prod.playlists.ihrhls.com/2397_icy'
        # url = 'https://c3.prod.playlists.ihrhls.com/2397/playlist.m3u8?listeningSessionID=5d3b60b8fcb8698c_2076473_RoovGj2f__0000001vIqY&downloadSessionID=0&at=0&birthYear=null&campid=header&cid=index.html&clientType=web&fb_broadcast=0&host=webapp.US&init_id=8169&listenerId=11a7ea3a3ba17c4ef971a7717be61ace&modTime=1566248899495&pname=15400&profileid=1156407194&territory=US&uid=1565113148810&age=null&gender=null&amsparams=playerid%3AiHeartRadioWebPlayer%3Bskey%3A1566248899&terminalid=159&awparams=g%3Anull%3Bn%3Anull%3Bccaud%3Aundefined%3BcompanionAds%3Atrue&playedFrom=6&dist=iheart&devicename=web-desktop&stationid=2397'
        ending = '.aac'
    
    return url, ending

def get_file_path(song_name, station, dest, audio_type, ending):
    """Generates a valid path for a song name.
    Args:
        song_name (str): the name of the song
        station (str): the genre of music
        dest (str): the destination for the song files
        audio_type (str): the type of audio (['radio', 'stream'])
        ending (str): the file ending
    """
    today = datetime.today()
    year, month, day = str(today.year), str(today.month), str(today.day)

    file_path = os.path.join(dest, '_'.join([year, month, day, station, audio_type, song_name]))

    # If the path already exists, add a suffix padded with zeros
    if os.path.exists(file_path + '.wav'):

        i = 0
        while os.path.exists(file_path + str(i).zfill(3) + '.wav'):
            i += 1

        return file_path + str(i).zfill(3) + ending

    return file_path + ending

def get_song_name(station):
    """Gets the name of the song currently being streamed from a website. Adapted from:
    https://stackoverflow.com/questions/35102278/python-3-get-song-name-from-internet-radio-stream
    Args:
        station (str): the category of music ('rock', 'classical', 'talk', 'country')
    """
    url, _ = get_url(station)
    encoding = 'iso-8859-1' # default: iso-8859-1 for mp3 and utf-8 for ogg streams
    req = request.Request(url, headers={'Icy-MetaData': 1})  # request metadata
    response = request.urlopen(req)
    metaint = int(response.headers['icy-metaint'])

    loop_limit = 10
    for i in range(loop_limit): # title may be empty initially, try several times

        response.read(metaint)  # skip to metadata
        metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
        metadata = response.read(metadata_length).rstrip(b'\0')

        if station == 'talk':
            hour = datetime.now().hour
            return str(hour).zfill(2) + '00'
        elif station == 'rock':
            metadata = metadata.decode(encoding, errors='ignore')
            # print(metadata)
            try:
                artist = re.search(r'StreamTitle(.*?)text', metadata).group(1)
                song_title = re.search(r'text(.*?)song_spot', metadata).group(1)
                return convert_to_filestring(artist + song_title)
            except AttributeError:
                if i == loop_limit - 1:
                    return 'NoSongNameGiven'
                continue
        else:
            # extract title from the metadata
            m = re.search(br"StreamTitle='([^']*)';", metadata)
            if m:
                title = m.group(1)
                if title:
                    return convert_to_filestring(title.decode(encoding, errors='ignore'))

def monitor_song_name(station, duration, break_on_song):
    """Monitors the song name currently streamed at a given url, returns when the song changes
    or after 20 minute timeout.
    Args:
        station (str): the station to check for the song name
        duration (int): the maximum song length in minutes
        break_on_song (bool): whether to break on song changes
    Returns:
        new_song (str): the name of the new song
    """
    song = get_song_name(station)
    start_time = time.time()
    while True:
        time.sleep(1)
        for i in range(10):
            try:
                new_song = get_song_name(station)
                break
            except (RemoteDisconnected, HTTPError):
                time.sleep(1)
                print("remote disconnected, attempt:", i)

        if break_on_song and new_song != song:
            return new_song
        if (time.time() - start_time) > (60*duration):
            return new_song
        


def convert_to_filestring(name):
    """Normalizes string, converting non-alphanumeric characters to underscores.
    Copied from: https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    Args:
        name (str): a string possibly containing invalid characters for file names
    Returns:
        name (str): the string with all non-alphanumeric characters removed
    """
    name = "".join(x for x in name if x.isalnum())
    return name

# Unused
def get_metadata(station):
    """Gets the sample rate, bit rate, and number of channels from a classical station"""
    url, _ = get_url(station)

    req = request.Request(url, headers={'Icy-MetaData': 1})  # request metadata
    response = request.urlopen(req)
    audio_info = response.headers['ice-audio-info']
    sample_rate, bit_rate, channels = audio_info.split(';')
    sample_rate, bit_rate, channels = sample_rate.split('=')[1], bit_rate.split('=')[1], channels.split('=')[1]
    return sample_rate, bit_rate, channels