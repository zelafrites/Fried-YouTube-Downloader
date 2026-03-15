## LIB
from pytubefix import YouTube
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import threading

## FUNC

# Progress callback, called automatically by pytubefix during download
def on_progress(stream, chunk, bytes_remaining):

    # Total size of the file being downloaded (in bytes)
    total_size = stream.filesize
    # Calculate how many bytes have already been downloaded
    bytes_downloaded = total_size - bytes_remaining
    # Convert the progress into a percentage
    percentage = (bytes_downloaded / total_size) * 100

    # Update the GUI progress bar value
    progress_bar["value"] = percentage

    # Force the GUI to refresh so the progress bar visibly updates
    root.update_idletasks()

# Main function behind downloading the video
def download(link):

    yt_obj = YouTube(link, on_progress_callback=on_progress)
    yt_stream = yt_obj.streams.get_highest_resolution()

    path = Path.home() / "Downloads"

    try:
        yt_stream.download(path)
        print("Your video has been downloaded!")
        progress_bar["value"] = 100
    except Exception as e:
        print("Download Error, ", e)

# Function triggered by the button
def start_download():

    # Reset the progress bar before starting
    progress_bar["value"] = 0

    # Get the link from the entry box
    link = entry1.get()

    # Clear entry bar
    entry1.delete(0, tk.END)

    # Run the download function in a separate thread
    threading.Thread(target=download, args=(link,), daemon=True).start()

## MAIN

# Creates the main application window
root = tk.Tk()

# Set window size
root.geometry("500x200")
root.title("Fried YouTube Downloader")

# Add a visual header, define where it goes, text and its font alongside size
header = tk.Label(root, text="Fried YouTube Downloader", font=("Helvetica", 15))
header.pack(pady=5)

# Make a line to separate header from downloader
canvas = tk.Canvas(root, width=200, height=30)
canvas.pack()
canvas.create_line(0, 10, 200, 10)

# Add an entry box
tk.Label(root, text="YouTube Link").pack()
entry1 = tk.Entry(root, width=50)
entry1.pack(pady=1)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=2)

# Download button
download_btn = tk.Button(root, text="Download", command=start_download)
download_btn.pack(pady=5)

# Starts the event loop
root.mainloop()
