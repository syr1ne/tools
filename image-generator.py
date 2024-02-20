#!/usr/bin/env python3

import tkinter as tk
from PIL import ImageTk
from urllib.request import urlopen
from tkinter.filedialog import asksaveasfilename 
from tkinter import *

root = tk.Tk()
root.title("image generator")
root.geometry("400x400")

def refresh():
    imageUrl = None
    photo = None
    tag_var = tag.get()
    tag_var = tag_var.replace(" ", "+")
    resolution_var = resolution.get()
    global label
    label.destroy()
    imageUrl = f"https://source.unsplash.com/{resolution_var}/?{tag_var}"
    u = urlopen(imageUrl)
    global raw_data
    raw_data = u.read()
    u.close()

    photo = ImageTk.PhotoImage(data=raw_data)
    label = tk.Label(image=photo)
    label.image = photo
    label.pack()

def save():
    file_name = asksaveasfilename(defaultextension=".jpg")
    if not file_name:
        return
    with open(file_name, "wb") as file:
        file.write(raw_data)

tag_label = tk.Label(root, text="tags: ")
tag_label.pack(side=TOP)
tag = Entry(root)
tag.pack(side=TOP)
resolution_label = tk.Label(root, text="resolution: ")
resolution_label.pack(side=TOP)
resolution = Entry(root)
resolution.pack(side=TOP)
refreshButton = tk.Button(root, text="Refresh", command=refresh)
refreshButton.pack(side=LEFT)
saveButton = tk.Button(root, text="Save", command=save)
saveButton.pack(side=RIGHT)


imageUrl = "https://source.unsplash.com/daily/"
u = urlopen(imageUrl)
global raw_data
raw_data = u.read()
u.close()

photo = ImageTk.PhotoImage(data=raw_data)
label = tk.Label(image=photo)
label.image = photo
label.pack()

root.mainloop()

