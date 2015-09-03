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
	#print visible_text
	start = [m.start() for m in re.finditer('RISE AGAINST LYRICS', visible_text)][0]
	end = [m.start() for m in re.finditer(' Submit Corrections', visible_text)][0]
	lyrics = visible_text[start+24:end-14]
	print "Got lyrics for "+song
	f = open("lyrics/"+song+".txt", "w+")
	try:
		f.write(lyrics)
	except:
		pass
	f.close()

def search_for(search_term, exact_flag):
	letters = "abcdefghijklmnopqrstuvwxyz"
	all_songs = os.listdir(sys.path[0]+"/lyrics")
	match_lines = []
	search_term = search_term.lower()
	for song_file in all_songs:
		f = open("lyrics/"+song_file)
		lines = list(f)
		f.close()
		for i in range(len(lines)):
			line = lines[i].lower()
			if search_term in line and line not in match_lines:
				context = line
				if exact_flag:
					index = context.index(search_term)
					if index != 0 and context[index-1] in letters:
						print context
						break
					if index != len(context)-len(search_term) and context[index+len(search_term)] in letters:
						break
				match_lines.append(context)
				if i != 0:
					context = lines[i-1] + context
				if i != len(lines)-1:
					context += lines[i+1]
				print_match(lines[0],context)

def get_stats():
	all_songs = os.listdir(sys.path[0]+"/lyrics")
	freq = {}
	longest_word = ""
	longest_word_songfile = ""
	word_lengths = []
	title_lens = []
	for song_file in all_songs:
		f = open("lyrics/"+song_file)
		lines = list(f)
		f.close()
		title = lines[0]
		title_lens.append(len(title.split(" ")))
		for i in range(len(lines)):
			line = lines[i].lower()
			words = line.split(" ")
			for word in words:
				if word in freq:
					freq[word] +=1
				else:
					freq[word] = 1
				if len(word) > len(longest_word) and "-" not in word:
					longest_word = word
					longest_word_songfile = title
				word_lengths.append(len(word))
	sorted_most_common = sorted(freq, key=freq.get, reverse=True)
	print "100 Most Common Words:"
	for word in sorted_most_common[0:100]:
		print word + " (" + str(freq[word]) + ")"
	print "\nLongest Word: " + longest_word + " in " + longest_word_songfile
	print "Average word length: " + str(sum(word_lengths)/len(word_lengths))
	print "Average title length: " + str(sum(title_lens)/len(title_lens))

def print_match(title, context):
	print title.strip() + " contains a match!"
	print context

if __name__ == "__main__":
	#get_stats()
	#get_all_lyrics()
	exact_flag = False
	if len(sys.argv) == 3:
		exact_flag = True
	search_for(sys.argv[1], exact_flag)

