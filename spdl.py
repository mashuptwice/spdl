#!/usr/bin/env python
import time, requests, os, subprocess, re, yt_dlp, natsort, shutil

url_base_en="https://www.southpark.de/en/seasons/south-park"

os.makedirs("dl", exist_ok=True)
os.makedirs("dl/tmp", exist_ok=True)

res_seasons = requests.get(url_base_en)
res_seasons.raise_for_status()

#get the "magic" string of the season
#\\u002F(?P<code>[a-zA-Z0-9]+)\\u002Fseason-


seasonnr = input("Which season do you want to download: ")

seasonexp = "\\u002F(?P<code>[a-zA-Z0-9]+)\\u002Fseason-"
matches=re.search(seasonexp + seasonnr, res_seasons.text)
seasoncode=matches.group("code")
#print(seasoncode)
#craft a url
url="https://www.southpark.de/en/seasons/south-park/" + seasoncode + "/season-" + seasonnr
#print(url)

#get the episodes urls 
res_episodes = requests.get(url)
res_episodes.raise_for_status()
episodeexp = "href=\"(?P<episodeurl>/en/episodes/[a-z0-9]+/(?P<episodename>[a-z0-9-]+))\""

episodeurls = []
episodenames = []

for i in re.finditer(episodeexp, res_episodes.text):
        #print(i.group("episode"))
        episodeurls.append("https://southpark.de" + i.group("episodeurl"))
        episodenames.append(i.group("episodename"))

#print(episodeurls)
#print(episodenames)

count = 1
for i in episodenames:
        print(str(count) + ":  " + i)
        count += 1


episodenr = input("select one episode to download: "
        )
#download the episode

os.chdir("dl/tmp")

ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(episodeurls[int(episodenr)-1])


#the episodes get downloaded as multiple files. Prepare a list of all parts for further processing with ffmpeg
try:
        os.remove("list.txt")
except OSError:
        pass
files = natsort.natsorted(os.listdir())
f = open("list.txt", "a")
for i in files:
        f.write("file " + "\'" + i + "\'" + "\n")
f.write("\n")
f.close()


#concat using ffmpeg
subprocess.Popen(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'out.mp4']).wait()

#rename and move the file out of the temp directory
os.rename("out.mp4", "../" + episodenames[int(episodenr)-1] + ".mp4")

#clean tmp directory
os.chdir("../")
shutil.rmtree("tmp")


print("finished")
