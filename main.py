import tkinter as tk
from pytube import YouTube
from moviepy.editor import VideoFileClip
from PIL import ImageTk, Image
import requests
from io import BytesIO


def show_video_info():
    link = link_entry.get()
    try:
        youtubeObject = YouTube(link)
        title_label.config(text="Title: " + youtubeObject.title)
        
        thumbnail_url = youtubeObject.thumbnail_url
        response = requests.get(thumbnail_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((150, 150))
        thumbnail = ImageTk.PhotoImage(img)
        thumbnail_label.config(image=thumbnail)
        thumbnail_label.image = thumbnail
        
    except Exception as e:
        status_label.config(text="An error has occurred: " + str(e))


def download_and_convert():
    link = link_entry.get()
    selected_format = format_var.get()
    try:
        yt = YouTube(link)
        title = yt.title
        status_label.config(text="Downloading...")
        stream = yt.streams.get_highest_resolution()
        filename = stream.download()
        status_label.config(text="Done.")
        if (selected_format == "MOV"):
            status_label.config(text="Converting to MOV...")
            clip = VideoFileClip(filename)
            new_filename = f"{title}.mov"
            clip.write_videofile(new_filename, codec="libx264")
            status_label.config(text=f"Download and conversion completed successfully: {new_filename}")
        if selected_format == "MP3":
            status_label.config(text="Converting to MP3...")
            clip = VideoFileClip(filename)
            audio_clip = clip.audio
            new_filename = f"{title}.mp3"
            audio_clip.write_audiofile(new_filename, codec="mp3")
            status_label.config(text=f"Download and conversion completed successfully: {new_filename}")

        
    except Exception as e:
        status_label.config(text="An error has occurred: " + str(e))
        print(str(e))

# Create main window
root = tk.Tk()
root.title("YT Video Downloader")

# Create entry widget for user to input the link
link_label = tk.Label(root, text="Enter the YouTube video URL:")
link_label.pack()
link_entry = tk.Entry(root, width=50)
link_entry.pack()

show_info_button = tk.Button(root, text="Show Video Info", command=show_video_info)
show_info_button.pack()


title_label = tk.Label(root, text="")
title_label.pack()

thumbnail_label = tk.Label(root)
thumbnail_label.pack()

format_label = tk.Label(root, text="Select format:")
format_label.pack()
formats = ["MP4", "MOV", "MP3"]
format_var = tk.StringVar(root)
format_var.set(formats[0])  # Default format
format_menu = tk.OptionMenu(root, format_var, *formats)
format_menu.pack()

download_button = tk.Button(root, text="Download", command=download_and_convert)
download_button.pack()


status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
