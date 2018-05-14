# Script for retriving members information from http://kmakishangarh.com/members-directory/
# and save it as csv to export data to google contacts

import urllib.request, urllib.parse, urllib.error
import ssl
from bs4 import BeautifulSoup
import csv

# to avoid ssl certificate issue
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

blank = ''

def find_trs(table, csv_name):

	csv_file = open(csv_name, 'w')
	writerobj = csv.writer(csv_file)
	writerobj.writerow(['Name','Given Name','Additional Name','Family Name','Yomi Name','Given Name Yomi','Additional Name Yomi',
						'Family Name Yomi','Name Prefix','Name Suffix','Initials','Nickname','Short Name','Maiden Name','Birthday',
						'Gender','Location','Billing Information','Directory Server','Mileage','Occupation','Hobby','Sensitivity',
						'Priority','Subject','Notes','Group Membership','Phone 1 - Type', 'Phone 1 - Value', 'Phone 2 - Type', 
						'Phone 2 - Value','Phone 3 - Type','Phone 3 - Value', 'Address 1 - Type', 'Address 1 - Formatted', 'Address 1 - Street',
						'Organization 1 - Type', 'Organization 1 - Name', ])
	tbody = table.find('tbody')
	trs = tbody.find_all('tr')
	
	print("Writing for %s" % csv_name)
	
	for tr in trs:
		unit = tr.find('td', {'class': 'column-1'})
		name = tr.find('td', {'class': 'column-2'})
		address = tr.find('td', {'class': 'column-3'})
		phone_o = tr.find('td', {'class': 'column-4'})
		phone_r = tr.find('td', {'class': 'column-5'})
		mobile = tr.find('td', {'class': 'column-6'})

		writerobj.writerow([name.text, name.text,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,
							blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,'* My Contacts','Mobile',mobile.text,'office',phone_o.text,
							'home', phone_r.text, 'Work', blank,address.text, 'Work', unit.text])

	csv_file.close()

url = "http://kmakishangarh.com/members-directory/"

html = urllib.request.urlopen(url, context=ctx)
soup = BeautifulSoup(html, 'html.parser')


gangsaw = soup.find('table', id="tablepress-1")
granite = soup.find('table', id="tablepress-2")
edgecutting = soup.find('table', id="tablepress-3")
crusher = soup.find('table', id="tablepress-4")


print("############### FOR GANG SAW ###################")
find_trs(gangsaw, 'gang_saw.csv')
print("############### FOR GRANITE ###################")
find_trs(granite, 'granite.csv')
print("############### FOR EDGE CUTTING ###################")
find_trs(edgecutting, 'edge_cutting.csv')
print("############### FOR CRUSHER TABLE ###################")
find_trs(crusher, 'crusher.csv')

