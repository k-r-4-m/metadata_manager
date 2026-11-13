from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from tkinter import ttk
import glob  
import numpy as np
from numpy import loadtxt

with open('genres.txt', 'r') as file:
    # get list of all genres in saved file
    lines = file.readlines()

# makes 'year' a writable tag
EasyID3.RegisterTextKey('year', 'TDRC')

# set up GUI first
root = tk.Tk()
width = root.winfo_screenwidth()               
height= root.winfo_screenheight()               
root.geometry("%dx%d" % (width, height))

label = tk.Label(root, text="Select Genre:")
label.pack()

# controls selection for combobox
def select(event):
    selected_item = combo_box.get()
    # label.config(text="Selected Item: " + selected_item)

# Create a Combobox widget
combo_box = ttk.Combobox(
    root,
    values=lines,
    state="readonly"
)
combo_box.pack(pady=5)

combo_box.set("")

combo_box.bind("<<ComboboxSelected>>", select)

tk.Label(root, text="Enter Genre Instead").pack()
entry1 = tk.Entry(root).pack()

button = tk.Button(root, text="Submit Genre", width=25, command=root.destroy)
button.pack()

tk.Label(root, text="Enter Year").pack()
entry2 = tk.Entry(root).pack()

button2 = tk.Button(root, text="Submit Year", width=25, command=root.destroy)
button2.pack()

# show the user the song name, artist, and album
song_label = tk.Label(root, text="")
artist_label = tk.Label(root, text="")
album_label = tk.Label(root, text="")
song_label.pack()
artist_label.pack()
album_label.pack()

# all_files = glob.glob("D:/Spotify Songs/all_songs/*")

all_files = glob.glob('C:/Users/Mark/Downloads/delete me/*')

# for each artist in the source dir...
for i in np.arange(0, len(all_files)):
    artist_name = all_files[i].split('\\')[-1]

    # gets list of albums per artist
    artist_albums = glob.glob(all_files[i] + "/*")

    # for each album per artist...
    for j in np.arange(0, len(artist_albums)):
        album_name = artist_albums[i].split('\\')[-1]

        # gets list of all songs in this artist's (i's) album
        album_songs = glob.glob(artist_albums[j] + "/*.mp3")

        # basic flag that flips if artwork has been shown
        # only need to show artwork once
        artwork_shown = False

        # for each song in this album...
        for k in np.arange(0, len(album_songs)):
            song_name = album_songs[i].split('\\')[-1]

            # using easyID3 for basic tags
            mp3file = MP3(album_songs[k], ID3=EasyID3)

            # if year or genre is missing, show them to the user for editing
            if mp3file.get('genre') is None or mp3file.get('year') is None:
                song_label['text'] = f"Song File Name: {song_name}"
                artist_label['text'] = f"Artist Name: {artist_name}"
                album_label['text'] = f"Album Name: {album_name}"
                                
                # need to load full ID3 tags to access album artwork
                tags = ID3(album_songs[k])

                artwork = tags.getall("APIC")

                if artwork and not artwork_shown:
                    image = Image.open(BytesIO(artwork[0].data))
                    image = image.resize((250, 250))

                    album_art = ImageTk.PhotoImage(image)

                    artwork_label = tk.Label(root, image=album_art)
                    artwork_label.pack()

                    # Prevent Python from garbage collecting the image
                    artwork_label.image = album_art
                    artwork_shown = True

                # mp3file['genre'] = ['Instrumental Hip-Hop']
                # mp3file['year'] = ['2020']

            mp3file.save()

        # this album is done, can show artwork again for next album
        artwork_shown = False


root.mainloop()