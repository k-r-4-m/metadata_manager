from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import ttk
import glob  
import numpy as np  

# makes 'year' a writable tag
EasyID3.RegisterTextKey('year', 'TDRC')

# set up GUI first
root = tk.Tk()
width = root.winfo_screenwidth()               
height= root.winfo_screenheight()               
root.geometry("%dx%d" % (width, height))

# controls selection for combobox
def select(event):
    selected_item = combo_box.get()
    # label.config(text="Selected Item: " + selected_item)

# Create a Combobox widget
combo_box = ttk.Combobox(
    root,
    # list of genres available
    values=["", "Option 1", "Option 2", "Option 3"],
    state="readonly"
)
combo_box.pack(pady=5)

combo_box.set("")

combo_box.bind("<<ComboboxSelected>>", select)

tk.Label(root, text="Enter Genre Instead").pack()
entry1 = tk.Entry(root).pack()

button = tk.Button(root, text="Submit Genre", width=25, command=root.destroy)
button.pack()

tk.Label(root, text="Enter Year Instead").pack()
entry2 = tk.Entry(root).pack()

button2 = tk.Button(root, text="Submit Year", width=25, command=root.destroy)
button2.pack()

all_files = glob.glob('all_files/*')

# # for each artist in the source dir...
# for i in np.arange(0, len(all_files)):
#     # gets list of albums per artist
#     artist_albums = glob.glob(all_files[i] + "/*")

#     # for each album per artist...
#     for j in np.arange(0, len(artist_albums)):
#         # gets list of all songs in this artist's (i's) album
#         album_songs = glob.glob(artist_albums[j] + "/*.mp3")

#         # basic flag that flips if artwork has been shown
#         # only need to show artwork once
#         artwork_shown = False

#         # for each song in this album...
#         for k in np.arange(0, len(album_songs)):
#             # using easyID3 for basic tags
#             mp3file = MP3(album_songs[k], ID3=EasyID3)

#             # if genre is missing, fill it in
#             if mp3file.get('genre') is None:
#                 mp3file['genre'] = ['Instrumental Hip-Hop']

#             # if year is missing, fill it in
#             if mp3file.get('year') is None:
#                 mp3file['year'] = ['2020']

#             mp3file.save()

#             # need to load full ID3 tags to access album artwork
#             tags = ID3(album_songs[k])

#             artwork = tags.getall("APIC")

#             if artwork and not artwork_shown:
#                 image = Image.open(BytesIO(artwork[0].data))
#                 image.show()
#                 artwork_shown = True

#         # this album is done, can show artwork again for next album
#         artwork_shown = False


root.mainloop()