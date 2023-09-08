# import tkinter
import customtkinter as ctk
from customtkinter import filedialog
from pytube import YouTube
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
app.geometry("780x580")
app.title("Youtube Downloader")
app.iconbitmap(sys.executable)


def clear():
    link.delete("0", "end")
    finishLabel.configure(text="")
    progressBar.set(0)
    pPercentage.configure(text="0%")
    title.configure(text="Insert a Youtube Link")
    downloaded.configure(text="")
    global DOWNLOAD_FOLDER
    DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"


def startdownload():
    choice = optionmenu.get()
    ytLink = link.get()
    if choice == choices[0]:
        try:
            ytObject = YouTube(ytLink, on_progress_callback=on_progress)
            title.configure(text=ytObject.title, text_color="white")
            # video = ytObject.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video = ytObject.streams.filter(res="720p", progressive=True).first()
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
            video = ytObject.streams.filter(res="720p", progressive=True).first()
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


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percetage_of_completion = bytes_downloaded / total_size * 100
    # print(percetage_of_completion)
    per = str(int(percetage_of_completion))
    dwn1 = str(round(bytes_downloaded * 0.000001, 2))
    dwn2 = str(int(total_size * 0.000001))
    downloaded.configure(text=dwn1 + " / " + dwn2 + " MB")
    downloaded.update()
    pPercentage.configure(text=per + "%")
    pPercentage.update()
    progressBar.set(float(percetage_of_completion) / 100)


def start_download():
    Thread(target=startdownload).start()


def cancel_download():
    sys.exit()

def show_download():
        # filename = "yt_2.py"
        os.startfile(DOWNLOAD_FOLDER, "explore")

# frame
frame_1 = ctk.CTkFrame(master=app)
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
link = ctk.CTkEntry(master=frame_1, width=550, height=35, textvariable=url_val)
link.pack(padx=10, pady=(10, 0))
try:
    link.insert(0, app.clipboard_get())
except:
    link.get()

# FInish label
finishLabel = ctk.CTkLabel(master=frame_1, text="")
finishLabel.pack(padx=10, pady=10)


# progress-bar
pPercentage = ctk.CTkLabel(master=frame_1, text="0%")
pPercentage.pack()


progressBar = ctk.CTkProgressBar(master=frame_1, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# downloaded
downloaded = ctk.CTkLabel(master=frame_1, text="")
downloaded.pack()

# optionmenu_var = ctk.StringVar(value="720")
choices = ["720", "480", "360", "Audio"]
optionmenu = ctk.CTkOptionMenu(master=frame_1, values=choices)
optionmenu.pack(padx=10, pady=10)

saveEntry = ctk.CTkButton(master=frame_1, text="Change Directory", command=openloc)
saveEntry.pack(pady=10, padx=10)

# download button
download_btn = ctk.CTkButton(master=frame_1, text="Download", command=startdownload)
download_btn.pack(pady=10, padx=10)

# Reveal folder where file is downloaded
show_btn = ctk.CTkButton(master=frame_1, text="Show Download", command=show_download)
show_btn.pack(pady=10, padx=10)

# clear button
clear_btn = ctk.CTkButton(master=frame_1, text="Clear", command=clear)
clear_btn.pack(pady=10, padx=10)

# Quit BUtton
cancel_btn = ctk.CTkButton(master=frame_1, text="Quit", command=cancel_download)
cancel_btn.pack(pady=10, padx=10)


em = emoji.emojize("Created with :growing_heart:  @Dev")
author = ctk.CTkLabel(master=frame_1, text=em, justify=ctk.LEFT, cursor="hand2")
author.pack(pady=10, padx=10)
author.bind(
    "<Button-1>",
    lambda e: webbrowser.open_new_tab(
        "http://www.linkedin.com/in/devendra-singh-08b613254"
    ),
)

app.mainloop()

