"""
Let us build a crawler
"""
import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
from sqlite3 import OperationalError
from sqlite3 import dbapi2 as sqlite

# Create a list of words to ignore
ignorewords=set(['the','of','to','and','a','in','is','it'])

class crawler:
	# Initialize the crawler with the name of database
	def __init__(self, dbname):
		self.con = sqlite.connect(dbname)

	def __del__(self):
		self.con.close()

	def dbcommit(self):
		self.con.commit()

	# Auxilliary function for getting an entry id and adding
	# it if it's not present
	def getentryid(self, table, field, value, createnew=True):
		return None

	# Index an individual page
	def addtoindex(self, url, soup):
		print("Indexing %s" % url)

	# Extract the text from an HTML page(no tags)
	def gettextonly(self, soup):
		return None

	# Seperate the words by any non-whitespace character
	def seperatewords(self, text):
		return None

	# Return true if this url is already
	def isindexed(self, url):
		return False

	# Add a link between two pages
	def addlinkref(self, urlFrom, urlTo, linkText):
		pass

	# Starting with a list of pages, do a breadth
	# first search to the given depth, indexing pages
	# as we go
	def crawl(self, pages, depth=2):
		for i in range(depth):
			newpages=set()
			for page in pages:
				try:
					c=urllib2.urlopen(page)
				except:
					print("Could not open %s" % page)
					continue
				try:
					soup = BeautifulSoup(c.read(), "html.parser")
				except UnicodeEncodeError:
					soup = BeautifulSoup(unicode(c.read()), "html.parser")
					continue

				self.addtoindex(page, soup)

				links=soup('a')
				for link in links:
					if('href' in dict(link.attrs)):
						url = urljoin(page, link['href'])
						if url.find("'")!=-1:	continue
						url = url.split('#')[0]	# remove location portion
						if url[0:4] == 'http' and not self.isindexed(url):
							newpages.add(url)
						linkText = self.gettextonly(link)
						self.addlinkref(page, url, linkText)
				self.dbcommit()

			pages=newpages

	# Create the databases tables
	def createindextables(self):
		commands = [
		'create table urllist(url)',
		'create table wordlist(word)'
		'create table wordlocation(urlid, wordid, location)',
		'create table link(fromid integer, toid integer)',
		'create table linkwords(wordid, linkid)',
		'create index wordidx on wordlist(word)'
		'create index urlidx on urllist(url)',
		'create index wordurlidx on wordlocation(wordid)',
		'create index urltoidx on link(toid)',
		'create index urlfromidx on link(fromid)'
		]

		for command in commands:
			try:
				self.con.execute('create table urllist(url)')
			except OperationalError: 
			    continue
		self.dbcommit()