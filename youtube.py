import customtkinter as ctk
from customtkinter import filedialog
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import os
import emoji
import webbrowser
from threading import Thread
import sys

# Location for downloading
DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"

def openloc():
    global DOWNLOAD_FOLDER
    DOWNLOAD_FOLDER = filedialog.askdirectory()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("780x610")
app.title("Youtube Downloader")
app.iconbitmap(sys.executable)

def clear():
    link_entry.delete(0, "end")
    link_entry_.delete(0, "end")
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
    try:
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        title.configure(text=ytObject.title, text_color="white")
        if choice == choices[0]:
            video = ytObject.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        elif choice == choices[1]:
            video = ytObject.streams.filter(res="480p", progressive=True).first()
        elif choice == choices[2]:
            video = ytObject.streams.filter(res="360p", progressive=True).first()
        elif choice == choices[3]:
            video = ytObject.streams.filter(abr="160kbps", progressive=False).first()
            video.download(DOWNLOAD_FOLDER, filename=ytObject.title + ".mp3")
            finishLabel.configure(text="Downloaded!")
            return
        video.download(DOWNLOAD_FOLDER)
        finishLabel.configure(text="Downloaded!")
    except Exception as e:
        finishLabel.configure(text=f"Download Error: {str(e)}", text_color="red")

def startdownloadplay():
    ytLink = link_entry_.get()
    playlist = Playlist(ytLink)
    PlayListLinks = playlist.video_urls
    N = len(PlayListLinks)
    finish_Label.configure(text="Hold on...")
    for i, link in enumerate(PlayListLinks):
        try:
            yt = YouTube(link, on_progress_callback=on_progressplay)
            title_.configure(text=yt.title, text_color="white")
            finish_Label.configure(text=f"Downloading... {i + 1} of {N}")
            video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
            video.download(DOWNLOAD_FOLDER)
        except Exception as e:
            finish_Label.configure(text=f"Download Error: {str(e)}", text_color="red")
    finish_Label.configure(text="Downloaded All", text_color="green")
    title_.configure(text="Insert a Youtube Playlist Link")
    down_loaded.configure(text="")
    pPercentage.configure(text="")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    dwn1 = str(round(bytes_downloaded * 0.000001))
    dwn2 = str(int(total_size * 0.000001))
    downloaded.configure(text=f"{dwn1} / {dwn2} MB")
    pPercentage.configure(text=f"{per}%")
    progressBar.set(float(percentage_of_completion) / 100)

def on_progressplay(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    dwn1 = str(round(bytes_downloaded * 0.000001))
    dwn2 = str(int(total_size * 0.000001))
    down_loaded.configure(text=f"{dwn1} / {dwn2} MB")
    pPercentage.configure(text=f"{per}%")
    progressBar.set(float(percentage_of_completion) / 100)

def start_download():
    Thread(target=startdownload).start()

def start_downloadplay():
    Thread(target=startdownloadplay).start()

def cancel_download():
    sys.exit()

def show_download():
    os.startfile(DOWNLOAD_FOLDER, "explore")

tabview = ctk.CTkTabview(master=app)
tabview.pack(padx=5, pady=(5, 0), expand=True)
tabview.add("Playlist")
tabview.add("Single")
tabview.set("Single")

frame_1 = ctk.CTkFrame(master=tabview.tab("Single"))
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

title = ctk.CTkLabel(master=frame_1, text="Insert a Youtube Link", font=ctk.CTkFont(size=20, weight="bold"))
title.pack(padx=10, pady=(40, 0))

url_val = ctk.StringVar()
link_entry = ctk.CTkEntry(master=frame_1, width=550, height=35, textvariable=url_val)
link_entry.pack(padx=10, pady=(10, 0))
try:
    link_entry.insert(0, app.clipboard_get())
except:
    link_entry.get()

finishLabel = ctk.CTkLabel(master=frame_1, text="")
finishLabel.pack()

pPercentage = ctk.CTkLabel(master=frame_1, text="0%")
pPercentage.pack(padx=5, pady=5)
progressBar = ctk.CTkProgressBar(master=frame_1, width=400)
progressBar.set(0)
progressBar.pack(padx=5, pady=5)

downloaded = ctk.CTkLabel(master=frame_1, text="")
downloaded.pack()

choices = ["720", "480", "360", "Audio"]
optionmenu = ctk.CTkOptionMenu(master=frame_1, values=choices)
optionmenu.pack(padx=5, pady=5)

saveEntry = ctk.CTkButton(master=frame_1, text="Change Directory", command=openloc)
saveEntry.pack(pady=5, padx=5)

download_btn = ctk.CTkButton(master=frame_1, text="Download", command=start_download)
download_btn.pack(pady=5, padx=5)

show_btn = ctk.CTkButton(master=frame_1, text="Show Download", command=show_download)
show_btn.pack(pady=5, padx=5)

clear_btn = ctk.CTkButton(master=frame_1, text="Clear", command=clear)
clear_btn.pack(pady=5, padx=5)

cancel_btn = ctk.CTkButton(master=frame_1, text="Quit", command=cancel_download)
cancel_btn.pack(pady=(5, 10), padx=5)

frame_2 = ctk.CTkFrame(master=tabview.tab("Playlist"))
frame_2.pack(pady=20, padx=60, fill="both", expand=True)

title_ = ctk.CTkLabel(master=frame_2, text="Insert a Youtube Playlist Link", font=ctk.CTkFont(size=20, weight="bold"))
title_.pack(padx=10, pady=(40, 0))

url_val_ = ctk.StringVar()
link_entry_ = ctk.CTkEntry(master=frame_2, width=550, height=35, textvariable=url_val_)
link_entry_.pack(padx=10, pady=(10, 0))
try:
    link_entry_.insert(0, app.clipboard_get())
except:
    link_entry_.get()

finish_Label = ctk.CTkLabel(master=frame_2, text="")
finish_Label.pack(pady=5)

pPercentage = ctk.CTkLabel(master=frame_2, text="0%")
pPercentage.pack(padx=5, pady=5)
progressBar = ctk.CTkProgressBar(master=frame_2, width=400)
progressBar.set(0)
progressBar.pack(padx=5, pady=5)

down_loaded = ctk.CTkLabel(master=frame_2, text="")
down_loaded.pack()

saveEntry = ctk.CTkButton(master=frame_2, text="Change Directory", command=openloc)
saveEntry.pack(pady=10, padx=10)

download_btn_ = ctk.CTkButton(master=frame_2, text="Download", command=start_downloadplay)
download_btn_.pack(pady=10, padx=10)

show_btn = ctk.CTkButton(master=frame_2, text="Show Download", command=show_download)
show_btn.pack(pady=10, padx=10)

clear_btn = ctk.CTkButton(master=frame_2, text="Clear", command=clear)
clear_btn.pack(pady=10, padx=10)

cancel_btn = ctk.CTkButton(master=frame_2, text="Quit", command=cancel_download)
cancel_btn.pack(pady=10, padx=10)

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