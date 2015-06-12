from pattern.web import *
import urllib2
from bs4 import BeautifulSoup
import re

def get_all_lyrics():
	f = open("ra_songs_all.txt")
	songs = list(f)
	f.close()

	g = Google()
	for song in songs:
		url = ""
		song = song.strip()
		for result in g.search("rise against lyrics "+song):
			if "http://www.azlyrics.com/" in result.url:
				url = result.url
				break
		if url != "":
			print "Found url for "+song
			download_song_lyrics(url, song)

def download_song_lyrics(url, song):
	try:
		html = urllib2.urlopen(url.strip()).read()
	except:
		print "COULD NOT GET LYRICS FOR "+song
		return
	soup = BeautifulSoup(html)
	[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
	visible_text = soup.getText()
	start = [m.start() for m in re.finditer('RISE AGAINST LYRICS', visible_text)][0]
	end = [m.start() for m in re.finditer(' Submit Corrections', visible_text)][0]
	lyrics = visible_text[start+24:end-14]
	print "Got lyrics for "+song
	f = open("lyrics/"+song+".txt", "w+")
	f.write(lyrics)
	f.close()

if __name__ == "__main__":
	get_all_lyrics()