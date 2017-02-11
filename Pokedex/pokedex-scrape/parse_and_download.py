# USAGE
# python parse_and_download.py --pokemon-list pokemon_list.html --sprites sprites

# import the necessary packages
from BeautifulSoup import BeautifulSoup
import argparse
import requests

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--pokemon-list", required = True,
	help = "Path to where the raw Pokemon HTML file resides")
ap.add_argument("-s", "--sprites", required = True,
	help = "Path where the sprites will be stored")
args = vars(ap.parse_args())

# construct the soup and initialize the list of pokemon
# names
soup = BeautifulSoup(open(args["pokemon_list"]).read())
names = []

# loop over all link elements
for link in soup.findAll("a"):
	# update the list of pokemon names
	names.append(link.text)

# loop over the pokemon names
for name in names:
	# initialize the parsed name as just the lowercase
	# version of the pokemon name
	parsedName = name.lower()

	# if the name contains an apostrophe (such as in
	# Farfetch'd, just simply remove it)
	parsedName = parsedName.replace("'", "")

	# if the name contains a period followed by a space
	# (as is the case with Mr. Mime), then replace it
	# with a dash
	parsedName = parsedName.replace(". ", "-")

	# handle the case for Nidoran (female)
	if name.find(u'\u2640') != -1:
		parsedName = "nidoran-f"

	# and handle the case for Nidoran (male)
	elif name.find(u'\u2642') != -1:
		parsedName = "nidoran-m"

	# construct the URL to download the sprite
	print "[x] downloading %s" % (name)
	url = "http://img.pokemondb.net/sprites/red-blue/normal/%s.png" % (parsedName)
	r = requests.get(url)

	# if the status code is not 200, ignore the sprite
	if r.status_code != 200:
		print "[x] error downloading %s" % (name)
		continue

	# write the sprite to file
	f = open("%s/%s.png" % (args["sprites"], name.lower()), "wb")
	f.write(r.content)
	f.close()