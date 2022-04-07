#!/usr/bin/env python
import requests, os, bs4, re, yt_dlp

url_base_en="https://www.southpark.de/en/seasons/south-park"

os.makedirs("dl", exist_ok=True)

res = requests.get(url_base_en)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
#print(str(soup))
data=str(soup)

#get the "magic" string of the season
#\\u002F(?P<code>[a-zA-Z0-9]+)\\u002Fseason-

seasonnr = "22"
baseseasonexp = "\\u002F(?P<code>[a-zA-Z0-9]+)\\u002Fseason-"
seasonexp = baseseasonexp + seasonnr
matches=re.search(seasonexp, data)
seasoncode=matches.group("code")
#print(seasoncode)
#craft a url
url="https://www.southpark.de/en/seasons/south-park/" + seasoncode + "/season-" + seasonnr
#print(url)

#get the episodes urls 
res_episodes = requests.get(url)
res_episodes.raise_for_status()
seasonsoup = str(bs4.BeautifulSoup(res_episodes.text, "html.parser"))
#print(seasonsoup)
episodeexp = "href=\"(?P<episode>/en/episodes/[a-z0-9]+/[a-z0-9-]+)\""

#matches = re.search(episodeexp, seasonsoup)

#episodes = matches.group("episode")
episodes = []
for i in re.finditer(episodeexp, seasonsoup):
	#print(i.group("episode"))
	episodes.append("https://southpark.de" + i.group("episode"))


print(episodes)

#download the episode

