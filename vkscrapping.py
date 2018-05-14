# Script for retriving information from http://www.vkiassociation.com/
# and save it as csv to export data to google contacts

import urllib.request, urllib.parse, urllib.error
import ssl
import csv
import re
from bs4 import BeautifulSoup

# to avoid ssl certificate issue
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# pattern for tag ids
person_pattern = re.compile("GridView1.*person")
company_pattern = re.compile("GridView1.*title")
address_pattern = re.compile("GridView1.*add")
contact_pattern = re.compile("GridView1.*contact")
email_pattern = re.compile("GridView1.*email")
website_pattern = re.compile("GridView1.*web")

blank = ''

def get_table(url):

	html = urllib.request.urlopen(url, context=ctx)
	soup = BeautifulSoup(html, 'html.parser')
	tables = soup.find_all('table', {'width':"750px"})
	table_list = []
	for table in tables:
		if len(table.attrs) == 1:
			table_list.append(table)

	return table_list


def create_file(csv_name, table_list):

	group = csv_name.split()
	group.pop()
	group = " ".join(group)
	group = "* " + group
	csv_name = csv_name.replace('/', '-')
	csv_name = 'scrp/' + csv_name + '.csv'

	print("Writing in %s" % csv_name)
	csv_file = open(csv_name, 'w')
	writerobj = csv.writer(csv_file)
	writerobj.writerow(['Name','Given Name','Additional Name','Family Name','Yomi Name','Given Name Yomi','Additional Name Yomi',
						'Family Name Yomi','Name Prefix','Name Suffix','Initials','Nickname','Short Name','Maiden Name','Birthday',
						'Gender','Location','Billing Information','Directory Server','Mileage','Occupation','Hobby','Sensitivity',
						'Priority','Subject','Notes','Group Membership', 'E-mail 1 - Type', 'E-mail 1 - Value','Phone 1 - Type', 
						'Phone 1 - Value', 'Phone 2 - Type', 'Phone 2 - Value', 'Address 1 - Type', 'Address 1 - Formatted', 
						'Address 1 - Street','Organization 1 - Type','Organization 1 - Name', 'Website 1 - Type', 'Website 1 - Value'])
	

	for li in table_list:
		
		company = li.find('span', id=company_pattern)
		address = li.find('span', id=address_pattern)
		contact = li.find('span', id=contact_pattern)
		email = li.find('span', id=email_pattern)
		website = li.find('span', id=website_pattern)
		person = li.find('span', id=person_pattern)

		contact = contact.text
		contact = contact.split(', ')
		if len(contact) > 1:
			contact1 = contact[0]
			contact2 = contact[1]
			
			contact1 = contact1.split('(')
			contact1 = '+91'+contact1[0]

			contact2 = contact2.split('(')
			contact2 = '+91'+contact2[0]
		else:
			contact = contact[0]
			contact = contact.split('(')
			contact1 = '+91'+contact[0]
			contact2 = blank

		writerobj.writerow([person.text, person.text,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,
			blank,blank,blank,blank,blank,blank,blank,blank,blank,blank,group,'Work', email.text,'Mobile',contact1,'office',contact2, 
			'Work', blank, address.text, 'Work', company.text, 'Work', website.text])

	csv_file.close()


url = "http://www.vkiassociation.com/"
html = urllib.request.urlopen(url, context=ctx)
soup = BeautifulSoup(html, 'html.parser')

tag = soup.find_all('a')
links = dict()
for link in tag:
	if link.get('href'):
		if link.get('href').startswith('associationmembers.aspx?group='):
			csv_name = link.text
			link = 'http://www.vkiassociation.com/' + link.get('href')
			links[csv_name] = link


for fl_name, link in links.items():
	print('fetching link', link)
	table_list = get_table(link)
	create_file(fl_name, table_list)

