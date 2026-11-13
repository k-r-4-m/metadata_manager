from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
from PIL import Image
from io import BytesIO

import glob  
  
import numpy as np  

# makes 'year' a writable tag
EasyID3.RegisterTextKey('year', 'TDRC')

# mp3file = MP3(all_files[0], ID3=EasyID3)   
# print(mp3file)
# mp3file['genre'] = ['G-Funk']
# mp3file['year'] = ['1996']

# mp3file.save()

# all_files = glob.glob("D:/Spotify Songs/all_songs/2Pac/All Eyez On Me/*.mp3")  

# for i in np.arange(0, len (all_files)):
# 	mp3file = MP3(all_files[i], ID3=EasyID3)
# 	mp3file['genre'] = ['G-Funk']
# 	mp3file['year'] = ['1996']
# 	mp3file.save()


all_files = glob.glob("D:/Spotify Songs/all_songs/*")
all_albums_0 = glob.glob(all_files[0] + "/*")
all_songs_0 = glob.glob(all_albums_0[0] + "/*.mp3")

for i in np.arange(0, len(all_songs_0)):
    mp3file = MP3(all_songs_0[i], ID3=EasyID3)

    if mp3file.get('genre') is None:
        mp3file['genre'] = ['Instrumental Hip-Hop']
        mp3file['year'] = ['2020']

    mp3file.save()

    # need to load full ID3 tags to access album artwork
    tags = ID3(all_songs_0[i])

    artwork = tags.getall("APIC")

    if artwork:
        image = Image.open(BytesIO(artwork[0].data))
        image.show()
    else:
        print(f"No artwork found: {all_songs_0[i]}")