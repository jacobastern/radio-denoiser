from datetime import datetime
import os

def get_file_path(genre, dest, audio_type, ending):
    """Generates a valid path for a song name.
    Args:
        genre (str): the genre of music
        dest (str): the destination for the song files
        audio_type (str): the type of audio (['radio', 'stream'])
        ending (str): the file ending
    """
    today = datetime.today()
    year, month, day = str(today.year), str(today.month), str(today.day)

    file_path = os.path.join(dest, '_'.join([year, month, day, genre, audio_type]))

    # If the path already exists, add a suffix padded with zeros
    if os.path.exists(file_path + '.wav'):

        i = 0
        while os.path.exists(file_path + str(i).zfill(3) + '.wav'):
            i += 1

        return file_path + str(i).zfill(3) + ending

    return file_path + ending