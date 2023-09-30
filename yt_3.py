# import tkinter
import customtkinter as ctk
from customtkinter import filedialog
from pytube import YouTube
from pytube import Playlist
import os
import emoji
import webbrowser
from threading import Thread
import sys

# location for downloading
DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"
# CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
## DOWNLOADS_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Downloads")


def openloc():
    global DOWNLOAD_FOLDER
    DOWNLOAD_FOLDER = filedialog.askdirectory()
    # locationnerror.config(text="Choose Directory", fg="red")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


app = ctk.CTk()
app.geometry("780x610")
app.title("Youtube Downloader")
app.iconbitmap(sys.executable)


def clear():
    link_entry.delete("0", "end")
    link_entry_.delete("0", "end")
    finishLabel.configure(text="")
    finish_Label.configure(text="")
    progressBar.set(0)
    pPercentage.configure(text="0%")
    title.configure(text="Insert a Youtube Link")
    title_.configure(text="Insert a Youtube Playlist Link")
    downloaded.configure(text="")
    down_loaded.configure(text="")
    global DOWNLOAD_FOLDER
    DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"


def startdownload():
    choice = optionmenu.get()
    ytLink = link_entry.get()
    if choice == choices[0]:
        try:
            ytObject = YouTube(ytLink, on_progress_callback=on_progress)
            title.configure(text=ytObject.title, text_color="white")
            # video = ytObject.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            # video = ytObject.streams.filter(res="720p", progressive=True).first()
            video = (
                ytObject.streams.filter(progressive=True, file_extension="mp4")
                .order_by("resolution")
                .desc()
                .first()
            )
            finishLabel.configure(text="")
            video.download(DOWNLOAD_FOLDER)
            finishLabel.configure(text="Downloaded!")
        except:
            finishLabel.configure(text="Download Error", text_color="red")
    elif choice == choices[1]:
        try:
            ytObject = YouTube(ytLink, on_progress_callback=on_progress)
            title.configure(text=ytObject.title, text_color="white")
            # video = ytObject.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video = ytObject.streams.filter(res="480p", progressive=True).first()
            finishLabel.configure(text="")
            video.download(DOWNLOAD_FOLDER)
            finishLabel.configure(text="Downloaded!")
        except:
            finishLabel.configure(text="Download Error", text_color="red")

    elif choice == choices[2]:
        try:
            ytObject = YouTube(ytLink, on_progress_callback=on_progress)
            title.configure(text=ytObject.title, text_color="white")
            # video = ytObject.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video = ytObject.streams.filter(res="360p", progressive=True).first()
            finishLabel.configure(text="")
            video.download(DOWNLOAD_FOLDER)
            finishLabel.configure(text="Downloaded!")
        except:
            finishLabel.configure(text="Download Error", text_color="red")
    elif choice == choices[3]:
        try:
            ytObject = YouTube(ytLink, on_progress_callback=on_progress)
            title.configure(text=ytObject.title, text_color="white")
            # audio = ytObject.streams.get_audio_only()
            audio = ytObject.streams.filter(abr="160kbps", progressive=False).first()
            finishLabel.configure(text="")
            audio.download(DOWNLOAD_FOLDER, filename=ytObject.title + ".mp3")
            finishLabel.configure(text="Downloaded!")
        except:
            finishLabel.configure(text="Download Error", text_color="red")


def startdownloadplay():
    # choice = optionmenu.get()
    ytLink = link_entry_.get()
    playlist = Playlist(ytLink)
    PlayListLinks = playlist.video_urls
    N = len(PlayListLinks)
    finish_Label.configure(text="Hold on...")
    for i, link in enumerate(PlayListLinks):
        try:
            # ytObject = YouTube(ytLink, on_progress_callback=on_progress)
            yt = YouTube(link, on_progress_callback=on_progressplay)
            title_.configure(text=yt.title, text_color="white")
            finish_Label.configure(text="Downloading... {0} of {1}".format(i, N))
            # video = ytObject.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            # video = yt.streams.filter(res="720p", progressive=True).first()
            video = (
                yt.streams.filter(progressive=True, file_extension="mp4")
                .order_by("resolution")
                .desc()
                .first()
            )
            video.download(DOWNLOAD_FOLDER)
            # finish_Label.configure(text="Downloading... {0} of {1}".format(i, N))
        except:
            finish_Label.configure(text="Download Error", text_color="red")
    finish_Label.configure(text="Downloaded All", text_color="green")
    title_.configure(text="Insert a Youtube Playlist Link")
    down_loaded.configure(text="")
    pPercentage.configure("")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percetage_of_completion = bytes_downloaded / total_size * 100
    # print(percetage_of_completion)
    per = str(int(percetage_of_completion))
    dwn1 = str(round(bytes_downloaded * 0.000001))
    dwn2 = str(int(total_size * 0.000001))
    downloaded.configure(text=dwn1 + " / " + dwn2 + " MB")
    downloaded.update()
    pPercentage.configure(text=per + "%")
    pPercentage.update()
    progressBar.set(float(percetage_of_completion) / 100)


def on_progressplay(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percetage_of_completion = bytes_downloaded / total_size * 100
    # print(percetage_of_completion)
    per = str(int(percetage_of_completion))
    dwn1 = str(round(bytes_downloaded * 0.000001))
    dwn2 = str(int(total_size * 0.000001))
    down_loaded.configure(text=dwn1 + " / " + dwn2 + " MB")
    down_loaded.update()
    pPercentage.configure(text=per + "%")
    pPercentage.update()
    progressBar.set(float(percetage_of_completion) / 100)


def start_download():
    Thread(target=startdownload).start()


def start_downloadplay():
    Thread(target=startdownloadplay).start()


def cancel_download():
    sys.exit()


def show_download():
    # filename = "yt_2.py"
    os.startfile(DOWNLOAD_FOLDER, "explore")


tabview = ctk.CTkTabview(master=app)
tabview.pack(padx=5, pady=(5, 0), expand=True)

tabview.add("Playlist")  # add tab at the end
tabview.add("Single")  # add tab at the end
tabview.set("Single")  # set currently visible tab
# frame1
frame_1 = ctk.CTkFrame(master=tabview.tab("Single"))
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

# label
title = ctk.CTkLabel(
    master=frame_1,
    text="Insert a Youtube Link",
    font=ctk.CTkFont(size=20, weight="bold"),
)
title.pack(padx=10, pady=(40, 0))

# link input
url_val = ctk.StringVar()
link_entry = ctk.CTkEntry(master=frame_1, width=550, height=35, textvariable=url_val)
link_entry.pack(padx=10, pady=(10, 0))
try:
    link_entry.insert(0, app.clipboard_get())
except:
    link_entry.get()

# FInish label
finishLabel = ctk.CTkLabel(master=frame_1, text="")
finishLabel.pack()


# progress-bar
pPercentage = ctk.CTkLabel(master=frame_1, text="0%")
pPercentage.pack(padx=5, pady=5)


progressBar = ctk.CTkProgressBar(master=frame_1, width=400)
progressBar.set(0)
progressBar.pack(padx=5, pady=5)

# downloaded
downloaded = ctk.CTkLabel(master=frame_1, text="")
downloaded.pack()

# optionmenu_var = ctk.StringVar(value="720")
choices = ["720", "480", "360", "Audio"]
optionmenu = ctk.CTkOptionMenu(master=frame_1, values=choices)
optionmenu.pack(padx=5, pady=5)

saveEntry = ctk.CTkButton(master=frame_1, text="Change Directory", command=openloc)
saveEntry.pack(pady=5, padx=5)

# download button
download_btn = ctk.CTkButton(master=frame_1, text="Download", command=start_download)
download_btn.pack(pady=5, padx=5)

# Reveal folder where file is downloaded
show_btn = ctk.CTkButton(master=frame_1, text="Show Download", command=show_download)
show_btn.pack(pady=5, padx=5)

# clear button
clear_btn = ctk.CTkButton(master=frame_1, text="Clear", command=clear)
clear_btn.pack(pady=5, padx=5)

# Quit BUtton
cancel_btn = ctk.CTkButton(master=frame_1, text="Quit", command=cancel_download)
cancel_btn.pack(pady=(5, 10), padx=5)

# frame 2
frame_2 = ctk.CTkFrame(master=tabview.tab("Playlist"))
frame_2.pack(pady=20, padx=60, fill="both", expand=True)

# label
title_ = ctk.CTkLabel(
    master=frame_2,
    text="Insert a Youtube Playlist Link",
    font=ctk.CTkFont(size=20, weight="bold"),
)
title_.pack(padx=10, pady=(40, 0))

# link input
url_val_ = ctk.StringVar()
link_entry_ = ctk.CTkEntry(master=frame_2, width=550, height=35, textvariable=url_val_)
link_entry_.pack(padx=10, pady=(10, 0))
try:
    link_entry_.insert(0, app.clipboard_get())
except:
    link_entry_.get()

# FInish label
finish_Label = ctk.CTkLabel(master=frame_2, text="")
finish_Label.pack(pady=5)


# progress-bar
pPercentage = ctk.CTkLabel(master=frame_2, text="0%")
pPercentage.pack(padx=5, pady=5)


progressBar = ctk.CTkProgressBar(master=frame_2, width=400)
progressBar.set(0)
progressBar.pack(padx=5, pady=5)


# downloaded
down_loaded = ctk.CTkLabel(master=frame_2, text="")
down_loaded.pack()


saveEntry = ctk.CTkButton(master=frame_2, text="Change Directory", command=openloc)
saveEntry.pack(pady=10, padx=10)

# download button
download_btn_ = ctk.CTkButton(
    master=frame_2, text="Download", command=start_downloadplay
)
download_btn_.pack(pady=10, padx=10)

# Reveal folder where file is downloaded
show_btn = ctk.CTkButton(master=frame_2, text="Show Download", command=show_download)
show_btn.pack(pady=10, padx=10)

# clear button
clear_btn = ctk.CTkButton(master=frame_2, text="Clear", command=clear)
clear_btn.pack(pady=10, padx=10)

# Quit BUtton
cancel_btn = ctk.CTkButton(master=frame_2, text="Quit", command=cancel_download)
cancel_btn.pack(pady=10, padx=10)


# author
em = emoji.emojize("Created with :growing_heart:  @Dev")
author = ctk.CTkLabel(master=app, text=em, justify=ctk.LEFT, cursor="hand2")
author.pack(pady=(0, 20), padx=5)
author.bind(
    "<Button-1>",
    lambda e: webbrowser.open_new_tab("https://www.instagram.com/rajputaashu25"),
)
author.bind(
    "<Button-1>",
    lambda e: webbrowser.open_new_tab("https://github.com/Dev7083"),
)

app.mainloop()
