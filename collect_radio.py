from datetime import datetime
import os

def get_radio_info(song_name, dest, root):

    today = datetime.today()
    year, month, day = str(today.year), str(today.month), str(today.day)

    if dest == 'classical':
        # 89.5 KBYU Classical
        radio_stream = tune_to('89.5')
        file_path = os.path.join(root, year + month + day + '_' + dest + '_' + song_name + '_radio' + '.mp3')
    
    elif dest == 'country':
        # 97.7 The Wolf
        radio_stream = tune_to('97,7')
        file_path = os.path.join(root, year + month + day + '_' + dest + '_' + song_name + '_radio' + '.mp3')
    
    elif dest == 'talk':
        # 102.7 KSL News Radio
        radio_stream = tune_to('102.7')
        file_path = os.path.join(root, year + month + day + '_' + dest + '_' + song_name + '_radio' + '.mp3')
    
    elif dest == 'rock':
        # 106.7 KAAZ-FM
        radio_stream = tune_to('106.7')
        file_path = os.path.join(root, year + month + day + '_' + dest + '_' + song_name + '_radio' + '.mp3')

    return radio_stream, file_path


def collect_radio(song_name, dest='rock', root='../../work/data/'):

    radio_stream, file_path = get_radio_info(song_name, dest, root)

    with open(file_path, 'wb') as f:
        print("File opened")
        try:
            for block in radio_stream.iter_content(1024):
                print("Received a block!")
                f.write(block)
        except KeyboardInterrupt:
            pass