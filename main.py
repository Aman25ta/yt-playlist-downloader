import pytube
import re,os,sys

import eyed3
from eyed3.id3.frames import ImageFrame
import subprocess
import requests

import time
import random,string

letters = string.ascii_lowercase
uid = ''.join(random.choice(letters) for i in range(6))


def process(song,artist,link,title,track_num,playlist_t):
   time.sleep(5)

   '''fmpeg -i "./songs/{playlist_t}/{title}".mp4 "./songs/{playlist_t}/{track_num}. {title}".mp3'''
   ppath = song.replace('.mp4','')
   ppath = ppath.replace('.mp3','')
   subprocess.run(f'C:/ffmpeg/bin/ffmpeg.exe -i \"{ppath}\".mp4 \"{ppath}\".mp3',shell=True)

   os.remove(f"{ppath}.mp4")

   newname = song.replace('.mp4', '.mp3')
   '''
   oldbase = os.path.splitext(song)
   output = os.rename(song, newname)
   '''
   
   img_data = requests.get(link).content
   with open(f'cover_{uid}.jpg', 'wb') as handler:
       handler.write(img_data)
      
   print(newname)
   audiofile = eyed3.load(newname)
   
   if (audiofile.tag == None):
       audiofile.initTag()
   
   audiofile.tag.title = title
   audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(f'cover_{uid}.jpg','rb').read(), 'image/jpeg')
   audiofile.tag.artist = artist
   audiofile.tag.track_num = track_num
   audiofile.tag.save()
   
   os.remove(f'cover_{uid}.jpg')

xurl = str(input("Enter url: "))

typ_dld = int(input("Enter 1 for mp3, 2 for mp4: "))
if typ_dld != 1 and typ_dld != 2:
   print("Invalid input")
   sys.exit()

playlist = pytube.Playlist(xurl)
c=1
rng = str(input(f"Enter range from 1-{len(playlist)} (split by - , includes both, 0 for none): "))
if rng!="0":
   n1 = rng.split("-")[0].strip(" ")
   n2 = rng.split("-")[1].strip(" ")
else:
   rng=0
   n1=n2=0
try:
   n1=int(n1)
   n2=int(n2)
except:
   print("Invalid range.")
   rng = 0
if typ_dld == 1:
   for url in playlist:
      if rng==0:
         ytt = pytube.YouTube(url)
         path = ytt.streams.get_audio_only().download(f"./songs/{playlist.title}",filename_prefix=f"{c}. ")
         process(f"./songs/{playlist.title}/"+path.split('\\')[-1],ytt.author,ytt.thumbnail_url,ytt._title,c,playlist.title)
         print(f"Downloaded: {c}. "+ytt._title)
      else:
         if c>=n1 and c<=n2:
            ytt = pytube.YouTube(url)
            path = ytt.streams.get_audio_only().download(f"./songs/{playlist.title}",filename_prefix=f"{c}. ")
            process(f"./songs/{playlist.title}/"+path.split('\\')[-1],ytt.author,ytt.thumbnail_url,ytt._title,c,playlist.title)
            print(f"Downloaded: {c}. "+ytt._title)
         elif c>n2:
            break
      c+=1
elif typ_dld ==2:
   capts=input("Type 1 to download captions, if they exist: ")
   for url in playlist:
      if rng==0:
         ytt = pytube.YouTube(url)
         path = ytt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download(f'./videos/{playlist.title}',filename_prefix=f"{c}. ")
         if capts =='1':
            caption = yt.captions.get_by_language_code('en')
            caption.download(srt=True,output_path=f'./videos/{playlist.title}')
         print(f"Downloaded: {c}. "+ytt._title)
      else:
         if c>=n1 and c<=n2:
            ytt = pytube.YouTube(url)
            path = ytt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download(f'./videos/{playlist.title}',filename_prefix=f"{c}. ")
            if capts =='1':
               caption = yt.captions.get_by_language_code('en')
               caption.download(srt=True,output_path=f'./videos/{playlist.title}')
            print(f"Downloaded: {c}. "+ytt._title)
         elif c>n2:
            break
      c+=1
print("Downloaded.")
