import pytube
import re,os


xurl = str(input("Enter url: "))

playlist = pytube.Playlist(xurl)
c=1
rng = str(input(f"Enter range from 1-{len(playlist)} (split by - , includes both, 0 for none): "))
if rng!="0":
   n1 = rng.split("-")[0].strip(" ")
   n2 = rng.split("-")[1].strip(" ")
else:
   rng=0
try:
   n1=int(n1)
   n2=int(n2)
except:
   print("Invalid range.")
   rng = 0
for url in playlist:
   if rng==0:
      ytt = pytube.YouTube(url)
      ytt.streams.get_audio_only().download("./songs",filename_prefix=f"{c}. ")
      print(f"Downloaded: {c}. "+ytt._title)
   else:
      if c>=n1 and c<=n2:
         ytt = pytube.YouTube(url)
         ytt.streams.get_audio_only().download("./songs",filename_prefix=f"{c}. ")
         print(f"Downloaded: {c}. "+ytt._title)
      elif c>n2:
         break
   c+=1

folder = './songs'
print("Converting...")
for filename in os.listdir(folder):
    infilename = os.path.join(folder,filename)
    if not os.path.isfile(infilename): continue
    oldbase = os.path.splitext(filename)
    newname = infilename.replace('.mp4', '.mp3')
    output = os.rename(infilename, newname)
print("Downloaded.")
