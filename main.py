import cv2
import string
import os
import tkinter as tk
from tkinter import filedialog

from stegano import lsb
from os.path import isfile, join

import time
import numpy as np
import math
import shutil
from subprocess import call, STDOUT

d = {}
c = {}
x = cv2
filename = string

for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)


# print(c)
def addFile():
    global x
    global filename
    # x = cv2.imread("1.jpg")
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("Images", "*.jpg; *.png"), ("Videos", "*.mp4")))
    x=cv2.imread(filename)


# i = x.shape[0]
# j = x.shape[1]
# print(i, j)

# key = input("Enter key to edit(Security Key) : ")
# text = input("Enter text to hide : ")
#
# kl = 0
# tln = len(text)
# z = 0  # decides plane
# n = 0  # number of row
# m = 0  # number of column
#
# l = len(text)
key=string
text=string
l=int
# Encrypt
def Encrypt():
    global key
    global text
    global l

    key = input("Enter key to edit(Security Key) : ")
    text = input("Enter text to hide : ")

    kl = 0
    tln = len(text)
    z = 0  # decides plane
    n = 0  # number of row
    m = 0  # number of column

    l = len(text)
    for i in range(l):
        x[n, m, z] = d[text[i]] ^ d[key[kl]]
        n = n + 1
        m = m + 1
        m = (m + 1) % 3  # this is for every value of z , remainder will be between 0,1,2 . i.e G,R,B plane will be set automatically.
        # whatever be the value of z , z=(z+1)%3 will always between 0,1,2 . The same concept is used for random number in dice and card games.
        kl = (kl + 1) % len(key)

    cv2.imwrite("encrypted_img.jpg", x)
    os.startfile("encrypted_img.jpg")
    print("Data Hiding in Image completed successfully.")


# x=cv2.imread(“encrypted_img.jpg")


# kl = 0
# tln = len(text)
# z = 0  # decides plane
# n = 0  # number of row
# m = 0  # number of column

# ch = int(input("\nEnter 1 to extract data from Image : "))


# decrypt.
def Decrypt():
    global key
    global text
    global l

    kl = 0
    tln = len(text)
    z = 0  # decides plane
    n = 0  # number of row
    m = 0  # number of column
    ch=1
    if ch == 1:
        key1 = input("\n\nRe enter key to extract text : ")
        decrypt = ""

        if key == key1:
            for i in range(l):
                decrypt += c[x[n, m, z] ^ d[key[kl]]]
                n = n + 1
                m = m + 1
                m = (m + 1) % 3
                kl = (kl + 1) % len(key)
            print("Encrypted text was : ", decrypt)
        else:
            print("Key doesn't match.")
    else:
        print("Thank you. EXITING.")

def VIDEO():
    def split_string(s_str, count=10):
        per_c = math.ceil(len(s_str) / count)
        c_cout = 0
        out_str = ''
        split_list = []
        for s in s_str:
            out_str += s
            c_cout += 1
            if c_cout == per_c:
                split_list.append(out_str)
                out_str = ''
                c_cout = 0
        if c_cout != 0:
            split_list.append(out_str)
        return split_list

    def frame_extraction(video):
        if not os.path.exists("./tmp"):
            os.makedirs("tmp")
        temp_folder = "./tmp"
        print("tmp directory is created")

        vidcap = cv2.VideoCapture(video)
        count = 0

        while True:
            success, image = vidcap.read()
            if not success:
                break
            cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
            count += 1

    def encode_string(input_string, root="./tmp/"):
        split_string_list = split_string(input_string)
        for i in range(0, len(split_string_list)):
            f_name = "{}{}.png".format(root, i)
            secret_enc = lsb.hide(f_name, split_string_list[i])
            secret_enc.save(f_name)
            print("frame {} holds {}".format(f_name, split_string_list[i]))

    def decode_string(video):
        #frame_extraction(video)
        secret = []
        root = "./tmp/"
        for i in range(len(os.listdir(root))):
            f_name = "{}{}.png".format(root, i)
            #print(f_name+"\n")
            secret_dec = lsb.reveal(f_name)
            if secret_dec == None:
                break
            secret.append(secret_dec)
        print("\nThe decoded text is: ")
        print(''.join([i for i in secret]))
        print("\n")
        #clean_tmp()

    def clean_tmp(path="./tmp"):
        if os.path.exists(path):
            shutil.rmtree(path)
            print("[INFO] tmp files are cleaned up")

    def main():
        input_string = input("Enter the input string :")
        f_name = input("Enter the name of the video: ")
        #f_name=filename
        #print(filename)
        frame_extraction(f_name)
        call(["ffmpeg", "-i", f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"], stdout=open(os.devnull, "w"),
             stderr=STDOUT)

        encode_string(input_string)
        # call(["ffmpeg", "-i", "tmp/%d.png", "-vcodec", "png", "tmp/video.mov", "-y"], stdout=open(os.devnull, "w"),
        #      stderr=STDOUT)

        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],
             stdout=open(os.devnull, "w"), stderr=STDOUT)
        # clean_tmp()

    if __name__ == "__main__":
        while True:
            print("1.Hide a message in video 2.Reveal the secret from video")
            print("any other value to exit")
            choice = input()
            if choice == '1':
                main()
            elif choice == '2':
                decode_string(input("enter the name of video with extension: "))
            else:
                break

root = tk.Tk()

canvas = tk.Canvas(root, height=300, width=300, bg="#5680E9")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# atDirectory = tk.IntVar()
# tick=tk.Checkbutton(root,text="Converted files at specified Directory", variable=atDirectory, onvalue=1, offvalue=0)
# tick.place(x=40, y=248)

OpenFile = tk.Button(root, text="Open File", padx=5, pady=2, fg="white", bg="#8860D0", command=addFile)
OpenFile.place(x=40, y=274)

toText = tk.Button(root, text="Encrypt", padx=5, pady=2, fg="white", bg="#8860D0", command=Encrypt)
toText.place(x=110, y=274)

concatenate = tk.Button(root, text="Decrypt", padx=5, pady=2, fg="white", bg="#8860D0", command=Decrypt)
concatenate.place(x=172, y=274)

video=tk.Button(root, text="Video", padx=5, pady=2, fg="white", bg="#8860D0", command=VIDEO)
video.place(x=101, y=2)

root.mainloop()
