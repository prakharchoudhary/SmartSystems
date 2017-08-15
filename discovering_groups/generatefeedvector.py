'''
An RSS feed is a simple XML document that contins information about
the blog and all the entries.
'''

import feedparser
import re
import sys

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
	# Parse the feed
	d = feedparser.parse(url)
	wc = {}

	# Loop over all the entries
	for e in d.entries:
		if 'summary' in e: summary=e.summary
		else: summary=e.description

		# Extract a list of words
		words = getwords(e.title+' '+summary)
		for word in words:
			wc.setdefault(word, 0)
			wc[word] += 1

	return getattr(d.feed, 'title', 'Unknown title'), wc

def getwords(html):
	# Remove all the HTML tags
	txt = re.compile(r'<[^>]+>').sub('', html)

	# Split words by all non-alpha characters
	words = re.compile(r'[^A-Z^a-z]+').split(txt)

	# Convert to lowercase
	return [word.lower() for word in words if word!='']


# loop over the feeds and generate the dataset
apcount = {}
wordcounts = {}
for feedurl in file('feedlist.txt'):
	title, wc = getwordcounts(feedurl)
	print("Generating wordcount list for {}\r".format(title.encode('utf-8')))
	wordcounts[title] = wc
	for word, count in wc.items():
		apcount.setdefault(word,0)
		if count>1:
			apcount[word]+=1

# Now include only the relevant words, since some like 'is' or 'the' will
# appear multiple time while a few will appear only once
wordlist = []
for w, bc in apcount.items():
	frac = float(bc)/len(feedlist)
	if frac>0.1 and frac<0.5: wordlist.append(w)


# Generate a text file containing a big matrix of all the word counts for each of the blogs
out = file('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
	out.write(blog)
	for word in wordlist:
		if word in wc:	out.write('\t%d' % wc[word])
		else:	out.write('\t0')
	out.write('\n') 