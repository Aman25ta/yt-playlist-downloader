import pytube
import re,os,sys

import eyed3
from eyed3.id3.frames import ImageFrame
import subprocess
import requests

import time
import random,string

import ffmpeg

letters = string.ascii_lowercase
uid = ''.join(random.choice(letters) for i in range(6))
def clean_filename(name):
        forbidden_chars = '"*\\/\'.|?:<>'
        filename = (''.join([x if x not in forbidden_chars else '' for x in name])).replace('  ', ' ').strip()
        if len(filename) >= 176:
            filename = filename[:170] + '...'
        return filename 
    
def download_video(link, path, res_level='FHD'):
    yt = pytube.YouTube(link)
    print(yt.title, '|', yt.author, '|', yt.publish_date.strftime("%Y-%m-%d"), '|', yt.views, '|', yt.length, 'sec')
    
    if res_level == '4K':
        dynamic_streams = ['2160p|160kbps', '1440p|160kbps', '1080p|160kbps', '720p|160kbps', '720p|128kbps', '480p|160kbps', '480p|128kbps']
    elif res_level == 'FHD':
        dynamic_streams = ['1080p|160kbps', '720p|160kbps', '720p|128kbps', '480p|160kbps', '480p|128kbps']
    for ds in dynamic_streams:
        try:
            yt.streams.filter(res=ds.split('|')[0], progressive=False).first().download(filename=f'video_{uid}.mp4',output_path="./temp")
            yt.streams.filter(abr=ds.split('|')[1], progressive=False).first().download(filename=f'audio_{uid}.mp3',output_path="./temp")
            break
        except:
            continue
    
    audio = ffmpeg.input(f'./temp/audio_{uid}.mp3')
    video = ffmpeg.input(f'./temp/video_{uid}.mp4')
    ffmpeg.output(audio, video, f'{path}.mp4').run(overwrite_output=True)

    os.remove(f"./temp/audio_{uid}.mp3")
    os.remove(f'./temp/video_{uid}.mp4')
    return

def process(song,artist,link,title,track_num,playlist_t):
   time.sleep(5)

   '''ffmpeg -i "./songs/{playlist_t}/{title}".mp4 "./songs/{playlist_t}/{track_num}. {title}".mp3'''
   ppath = song.replace('.mp4','')
   ppath = ppath.replace('.mp3','')
   subprocess.run(f'ffmpeg -i \"{ppath}\".mp4 \"{ppath}\".mp3',shell=True)

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
         process(f"./songs/{playlist.title}/"+path.split('\\')[-1],ytt.author,ytt.thumbnail_url,ytt.title,c,playlist.title)
         print(f"Downloaded: {c}. "+ytt.title)
      else:
         if c>=n1 and c<=n2:
            ytt = pytube.YouTube(url)
            path = ytt.streams.get_audio_only().download(f"./songs/{playlist.title}",filename_prefix=f"{c}. ")
            process(f"./songs/{playlist.title}/"+path.split('\\')[-1],ytt.author,ytt.thumbnail_url,ytt.title,c,playlist.title)
            print(f"Downloaded: {c}. "+ytt.title)
         elif c>n2:
            break
      c+=1
elif typ_dld ==2:
    resol = input("Enter resolution (if available, Default FHD);\n1: Upto FHD\n2: Upto 4k\n")
    for url in playlist:
        if rng==0:
            ytt = pytube.YouTube(url)
            if not ytt.title:
                continue
            try:
                os.mkdir('./videos')
            except:
                pass
            try:
                os.mkdir(f'./videos/{playlist.title}')
            except:
                pass
            download_video(url,f'./videos/{playlist.title}/{c}. {clean_filename(ytt.title)}','4K' if resol == "2" else "FHD")
            print(f"Downloaded: {c}. "+ytt.title)
        else:
            if c>=n1 and c<=n2:
                ytt = pytube.YouTube(url)
                if not ytt.title:
                    continue
                try:
                    os.mkdir('./videos')
                except:
                    pass
                try:
                    os.mkdir(f'./videos/{playlist.title}')
                except:
                    pass
                download_video(url,f'./videos/{playlist.title}/{c}. {clean_filename(ytt.title)}','4K' if resol == "2" else "FHD")
                print(f"Downloaded: {c}. "+ytt.title)
            elif c>n2:
                break
        c+=1
print("Downloaded.")
