import pygame.mixer as mixer
from tkinter import *
from tkinter import filedialog
import os

# Function to play the selected songs from the list or directory.
def play_song(song_name: StringVar, song_list: Listbox, status: StringVar):
    # Set the name of the current played song on the window.
    name = song_list.get(ACTIVE)
    if len(name) > 40:
        name = (name[:40] + '.mp3')
    song_name.set(name)

    # Load the selected song and start the mixer/play the song.
    mixer.music.load(song_list.get(ACTIVE))
    mixer.music.play()

    # Set the status of the player to Playing.
    status.set("Song Playing..")

    # Active the disabled resume button.
    if resume_btn['state'] == DISABLED:
        resume_btn['state'] = NORMAL

# Function to stop the current song and set the status of the player to 'stop'.
def stop_song(status: StringVar):
    mixer.music.stop()
    status.set("Song Stopped!!")

    # Disable the resume button when the song is stoped.
    resume_btn['state'] = DISABLED

# Function to pause the current song and set the status of the player to 'pause'.  
def pause_song(status: StringVar):
    mixer.music.pause()
    status.set("Song Paused!")

# Function to resume the paused song and set the status of the player to 'resume'.
def resume_song(status: StringVar):
    mixer.music.unpause()
    if status.get() == "<Not Available>":
        status.set("Please Select a song!")
    else:
        status.set("Song Playing..")

# Function to load all the songs from the specified directory. 
def load(listbox):
    # Request the user to input the path of the directory and os will change to that directory.
    os.chdir(filedialog.askdirectory(title="Open a song Directory"))
    
    # List all the songs present in the specified directory.
    tracks = os.listdir()

    # Takes all the songs from the directory and store in listbox.
    for track in tracks:
        listbox.insert(END, track)

# Function to change the sound volume.
def volume(x):
    value = volume_slider.get()
    mixer.music.set_volume(value/100)

# Starting the mixer.
mixer.init()

# Initializing the parent window of the GUI and set the resolution and the title of the GUI.
root = Tk()
root.geometry('700x220')
root.title('My Music Player')

# It helps to stop the change of the window size.
root.resizable(False, False)


# Creating the frames of the music player
song_frame = LabelFrame(root, text="Current song", bg='LightBlue', width=506, height=80)
song_frame.place(x=0, y=0)

button_frame = LabelFrame(root, text="Control Buttons", bg='Turquoise', width=506, height=120)
button_frame.place(y=80)

listbox_frame = LabelFrame(root, text='Playlist', bg="RoyalBlue", height=200, width=300)
listbox_frame.place(x=505, y=0)

volume_frame = LabelFrame(root, text="Volume", bg="Turquoise")
volume_frame.place(x=400, y=85)

# StringVar is used to manipulate text in entry, labels.
current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')

# Playlist Listbox.
playlist = Listbox(listbox_frame, font=('Helvetica', 11), selectbackground='Gold')

# Make the scroll bar to scroll the playlist.
scroll_bar = Scrollbar(listbox_frame, orient=VERTICAL)
scroll_bar.pack(side=RIGHT, fill=BOTH)
scroll_bar.config(command=playlist.yview)

playlist.config(yscrollcommand=scroll_bar.set)
playlist.pack(fill=BOTH, padx=5, pady=5)

# SongFrame labels.
Label(song_frame, text="CURRENTLY PLAYING: ", bg="LightBlue", font=('Times', 10, 'bold')).place(x=5, y=20)

song_lbl = Label(song_frame, textvariable=current_song, font=('Times', 12), bg='GoldenRod')
song_lbl.place(x=150, y=20)

# Buttons in the main screen.
pause_btn = Button(button_frame, text="Pause", bg='Aqua', font=('Georgia', 13), width=7, command=lambda: pause_song(song_status))
pause_btn.place(x=15, y=10)

stop_btn = Button(button_frame, text="Stop", bg='Aqua', font=("Georgia", 13), width=7, command=lambda: stop_song(song_status))
stop_btn.place(x=105, y=10)

play_btn = Button(button_frame, text="Play", bg='Aqua', font=("Georgia", 13), width=7, command=lambda: play_song(current_song, playlist, song_status))
play_btn.place(x=195, y=10)

resume_btn = Button(button_frame, text='Resume', bg="Aqua", font=("Georgia", 13), width=7, command=lambda: resume_song(song_status))
resume_btn.place(x=285, y=10)

dir_btn = Button(button_frame, text="Load Directory", bg='Aqua', font=("Georgia", 13), width=35, command=lambda: load(playlist))
dir_btn.place(x=10, y=55)

volume_slider = Scale(volume_frame, from_=100, to=0, orient=VERTICAL, command=volume, length=90, bg='orange', cursor='hand2')
volume_slider.set(30)
volume_slider.pack()

Label(root, textvariable=song_status, bg='SteelBlue', font=('Times', 8), justify=LEFT).pack(side=BOTTOM, fill=X)

# Finalize and start the main loop of the GUI.
root.update()
root.mainloop()