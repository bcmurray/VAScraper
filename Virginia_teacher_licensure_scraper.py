

# Import the packages we'll need to run the scraper
from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen
import csv
import time
import string


# We'll use this partial URL to build a 
url2 = 'https://p1pe.doe.virginia.gov/tinfo/getlicenseinfo.do?internal='

# TO MAKE THIS SCRAPER WORK, YOU'LL NEED TO SUPPLY YOUR OWN COOKIES!  Once you have authenticated one search, your JSESSIONID will be valid for 12+ hours 
cookies = 'JSESSIONID=NuLSgPiwiEAxd7Pr4_55gzIvjqBkNT9skFHO8pU_yRaNi3WRYrOX!722784394!1979284928'

# Start the counter at this number
counter = 865642

# This loop runs once for each value of "internal" from 865642 - 1500000
while counter < 1500000:
	
	# create an empty list to capture values from the resulting page and export them to CSV
	tempList = []

	# built the URL by converting the integer to string and appending it to the base URL
	url = 'https://p1pe.doe.virginia.gov/tinfo/getlicenseinfo.do?internal=' + str(counter)

	# Connect to the website
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', cookies))

	f = opener.open(url)

	# read the content of the resulting site
	content = f.read()
	
	# parse content using BeautifulSoup
	soup = BeautifulSoup(content)

	# Check to see if your cookies are expired, if so close the program and print the last result (change 'counter' to this value when restarting)
	quest = soup.find('legend')
	if quest:
		print "Loop failed at " + str(counter)
		break
	
	# Try to extract data if possible
	try: 
		bounding = soup.find_all('span', {'class' : 'fontbold'})

		for bounds in bounding:
			captured = bounds.find_next('span').get_text(strip=True)
			if captured != "":
				print captured
				tempList.append(str(captured))

	# if the "internal" ID value does not have a result, print 'none' and go to the next number of the loop
	except:
		print 'none'
		continue
	
	# if this iteration of the loop was able to extract data, write it to a CSV file
	if len(tempList):

		with open('VAteachers.csv', 'a') as outfile:
			wr = csv.writer(outfile, dialect='excel')
			wr.writerow(tempList)
			del tempList[:]
		
	# iterate the loop
	counter = counter + 1
	print counter




 
