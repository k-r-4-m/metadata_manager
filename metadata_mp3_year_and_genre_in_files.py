from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import glob
import os
import winsound

# makes 'year' a writable tag
EasyID3.RegisterTextKey('year', 'TDRC')

# loads genres
with open('genres.txt', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

# path for folder as global variable
folder_path = ""

# counter for current album being processed
current_album = 0

# allow user to select a directory and store it in global var
# called folder_path
def browse_button():
    global folder_path
    folder_path = filedialog.askdirectory()
    print(folder_path)


### GUI tkinter setup
class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        # creating a container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        # size of app's window
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height}")
 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
 
        # initializing frames to an empty array
        self.frames = {}  
 
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (BrowseSourceDirPage, Page1):
 
            frame = F(container, self)
 
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        # self.show_frame(BrowseSourceDirPage)

        frame = self.frames[BrowseSourceDirPage]
        frame.tkraise()
 
    # to display the current frame passed as parameter
    def show_frame(self, cont):
        # if folder path not selected, do nothing and play error sound
        if folder_path == "":
            winsound.MessageBeep(winsound.MB_ICONHAND)
        else:
            frame = self.frames[cont]
            frame.tkraise()
            frame.event_generate("<<ShowFrame>>")

# page for getting file path 
class BrowseSourceDirPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        # label of frame Layout 2
        label = ttk.Label(self, text ="Select source directory for music files")
        
        # putting the grid in its place by using
        # grid
        label.pack()

        # button to find source dir for music
        button2 = ttk.Button(self, text="Browse", command=browse_button)
        button2.pack()
 
        button1 = ttk.Button(self, text ="Continue", command=lambda: controller.show_frame(Page1))
        button1.pack()
 
 
# page for doing actual metadata editing
class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", self.run_metadata)

    def run_metadata(self, event):
        # only do this if folder path has been selected
        if folder_path != "":
            ### finds albums that require the metadata changes
            # i.e. doesnt have genre or year 
            all_files = glob.glob(folder_path + '/*')

            albums_to_edit = []

            for artist_folder in all_files:

                artist_name = os.path.basename(artist_folder)

                artist_albums = glob.glob(artist_folder + "/*")

                for album_folder in artist_albums:

                    album_name = os.path.basename(album_folder)

                    album_songs = glob.glob(album_folder + "/*.mp3")

                    # check whether any songs need metadata
                    needs_editing = False

                    for song in album_songs:
                        mp3file = MP3(song, ID3=EasyID3)

                        if mp3file.get('genre') is None or mp3file.get('year') is None:
                            needs_editing = True
                            break

                    if needs_editing and album_songs:

                        # Extract album artwork
                        tags = ID3(album_songs[0])
                        artwork = tags.getall("APIC")

                        artwork_data = artwork[0].data if artwork else None

                        albums_to_edit.append({
                            'artist': artist_name,
                            'album': album_name,
                            'songs': album_songs,
                            'artwork': artwork_data
                        })


            ### more GUI setup for info of metadata being edited
            # album information
            song_label = tk.Label(self, text="")
            artist_label = tk.Label(self, text="")
            album_label = tk.Label(self, text="")

            song_label.pack()
            artist_label.pack()
            album_label.pack()

            # artwork display
            artwork_label = tk.Label(self)
            artwork_label.pack()

            # genre selection
            tk.Label(self, text="Select Genre:").pack()

            combo_box = ttk.Combobox(
                self,
                values=lines,
                state="readonly"
            )
            combo_box.pack(pady=5)

            # custom genre
            tk.Label(self, text="Enter Genre Instead:").pack()

            entry1 = tk.Entry(self)
            entry1.pack()

            # year selection
            tk.Label(self, text="Enter Year:").pack()

            entry2 = tk.Entry(self)
            entry2.pack()

            # progress indicator
            progress_label = tk.Label(self, text="")
            progress_label.pack()


            ### displays current album
            def show_album():

                global current_album, album_art

                if current_album >= len(albums_to_edit):
                    song_label.config(text="All albums completed!")
                    artist_label.config(text="")
                    album_label.config(text="")
                    artwork_label.config(image="")
                    progress_label.config(text="")
                    return

                album = albums_to_edit[current_album]

                artist_name = album['artist']
                album_name = album['album']
                album_songs = album['songs']

                # Display album information
                song_label.config(text=f"Number of songs: {len(album_songs)}")
                artist_label.config(text=f"Artist: {artist_name}")
                album_label.config(text=f"Album: {album_name}")

                progress_label.config(
                    text=f"Album {current_album + 1} of {len(albums_to_edit)}"
                )

                # display album artwork
                if album['artwork']:

                    image = Image.open(BytesIO(album['artwork']))
                    image.thumbnail((250, 250))

                    album_art = ImageTk.PhotoImage(image)

                    artwork_label.config(image=album_art)
                    artwork_label.image = album_art

                else:
                    artwork_label.config(image="")
                    artwork_label.image = None

                # clear previous inputs
                combo_box.set("")
                entry1.delete(0, tk.END)
                entry2.delete(0, tk.END)


            ### saves metadata and moves onto next album
            def submit_metadata():

                global current_album

                if current_album >= len(albums_to_edit):
                    return

                # get selected genre or custom genre
                genre = entry1.get().strip()

                if not genre:
                    genre = combo_box.get().strip()

                year = entry2.get().strip()

                # validate inputs
                if not genre or not year:
                    print("Please enter a genre and year.")
                    return

                if not year.isdigit() or len(year) != 4:
                    print("Please enter a valid four-digit year.")
                    return

                album = albums_to_edit[current_album]

                # apply metadata to every song in the album
                for song in album['songs']:

                    mp3file = MP3(song, ID3=EasyID3)

                    # only fill missing metadata
                    if mp3file.get('genre') is None:
                        mp3file['genre'] = [genre]

                    if mp3file.get('year') is None:
                        mp3file['year'] = [year]

                    mp3file.save()

                print(f"Saved metadata for {album['album']}")

                # move to next album
                current_album += 1

                show_album()


            # submit button
            submit_button = tk.Button(
                self,
                text="Submit Metadata",
                width=25,
                command=submit_metadata
            )
            submit_button.pack(pady=10)

            ### starts the mainloop
            if albums_to_edit:
                show_album()
            else:
                song_label.config(text="No albums require metadata editing.")

        else:
            print("Folder path not found!")


app = tkinterApp()
app.mainloop()