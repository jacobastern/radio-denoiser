import re
from urllib import request
import struct
import time
import re
import unicodedata

def get_song_name(url):
    """Gets the name of the song currently being streamed from a given url"""
    encoding = 'iso-8859-1' # default: iso-8859-1 for mp3 and utf-8 for ogg streams
    req = request.Request(url, headers={'Icy-MetaData': 1})  # request metadata
    response = request.urlopen(req)
    metaint = int(response.headers['icy-metaint'])
    for _ in range(10): # # title may be empty initially, try several times
        response.read(metaint)  # skip to metadata
        metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
        metadata = response.read(metadata_length).rstrip(b'\0')
        # extract title from the metadata
        m = re.search(br"StreamTitle='([^']*)';", metadata)
        if m:
            title = m.group(1)
            if title:
                break

    return convert_to_filestring(title.decode(encoding, errors='ignore'))


def monitor_song_name(url):
    """Monitors the song name currently streamed at a given url, returns when the song changes"""
    song = get_song_name(url)
    while True:
        new_song = get_song_name(url)
        if new_song != song:
            return new_song
        time.sleep(.2)

def convert_to_filestring(name):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    Copied from: https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    """
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
    name = unicode(re.sub('[^\w\s-]', '', name).strip().lower())
    name = unicode(re.sub('[-\s]+', '-', name))
    return name