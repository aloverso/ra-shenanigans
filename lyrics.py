from pattern.web import *
import urllib2
from bs4 import BeautifulSoup
import re
import os
import sys

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
	print url.strip()
	html = urllib2.urlopen(url.strip()).read()
	soup = BeautifulSoup(html)
	[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
	visible_text = soup.getText()
	print visible_text
	'''start = [m.start() for m in re.finditer('RISE AGAINST LYRICS', visible_text)][0]
	end = [m.start() for m in re.finditer(' Submit Corrections', visible_text)][0]
	lyrics = visible_text[start+24:end-14]
	print "Got lyrics for "+song
	f = open("lyrics/"+song+".txt", "w+")
	f.write(lyrics)
	f.close()'''

def search_for(search_term):
	all_songs = os.listdir(sys.path+"/lyrics")
	for song_file in all_songs:
		f = open(song_file)
		lines = list(f)
		f.close()
		for i in range(len(lines)):
			line = lines[i]
			if search_term in line:
				context = line
				if i != 0:
					context += lines[i-1]
				if i != len(lines)-1:
					context += lines[i+1]
				print_match(lines[0],context)

def print_match(title, content):
	print title + " contains a match!"
	print context

if __name__ == "__main__":
	get_all_lyrics()
