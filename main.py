import pytube
import re,os

import eyed3
from eyed3.id3.frames import ImageFrame
import subprocess
import requests

import time

def process(song,artist,link,title,track_num):
   time.sleep(5)

   '''fmpeg -i "./songs/{title}".mp4 "./songs/{track_num}. {title}".mp3'''
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
   with open('cover.jpg', 'wb') as handler:
       handler.write(img_data)
      
   print(newname)
   audiofile = eyed3.load(newname)
   
   if (audiofile.tag == None):
       audiofile.initTag()
   
   audiofile.tag.title = title
   audiofile.tag.images.set(ImageFrame.FRONT_COVER, open('cover.jpg','rb').read(), 'image/jpeg')
   audiofile.tag.artist = artist
   audiofile.tag.track_num = track_num
   audiofile.tag.save()
   
   os.remove('cover.jpg')

xurl = str(input("Enter url: "))

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
for url in playlist:
   if rng==0:
      ytt = pytube.YouTube(url)
      path = ytt.streams.get_audio_only().download("./songs",filename_prefix=f"{c}. ")
      process("./songs/"+path.split('\\')[-1],ytt.author,ytt.thumbnail_url,ytt._title,c)
      print(f"Downloaded: {c}. "+ytt._title)
   else:
      if c>=n1 and c<=n2:
         ytt = pytube.YouTube(url)
         path = ytt.streams.get_audio_only().download("./songs",filename_prefix=f"{c}. ")
         process("./songs/"+path.split('\\')[-1],ytt.author,ytt.thumbnail_url,ytt._title,c)
         print(f"Downloaded: {c}. "+ytt._title)
      elif c>n2:
         break
   c+=1

folder = './songs' 
print("Downloaded.")
