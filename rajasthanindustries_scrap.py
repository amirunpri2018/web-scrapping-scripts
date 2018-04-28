import urllib.request, urllib.parse, urllib.error
import ssl
import re
import csv
from bs4 import BeautifulSoup

# to avoid ssl certificate issue
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

company_pattern = re.compile('ct.*companyname')
address_pattern = re.compile('ct.*lbl_address')
phone_pattern = re.compile('ct.*lbl_ph')
mobile_pattern = re.compile('ct.*lbl_mobile')
contact_person_pattern = re.compile('ct.*lbl_contactper')

csv_file = open('company_detail.csv', 'a')
writerobj = csv.writer(csv_file)
writerobj.writerow(['comapany_name', 'Address', 'Phone', 'Industry', 'Sub-Industry', 'Contact Person'])

def rajindus(url):
	
	html = urllib.request.urlopen(url, context=ctx)
	soup = BeautifulSoup(html, 'html.parser')

	tables = soup.find_all('td', {'width':'80%'})

	for table in tables:
		
		company = table.find('span', id=company_pattern)
		industry = "Weaving Units"
		address = table.find('span', id=address_pattern)
		phone = table.find('span', id=phone_pattern)
		mobile = table.find('span', id=mobile_pattern)
		contact_person = table.find('span', id=contact_person_pattern)
		sub_industry = '-'
		company_name = company.text
		address = address.text
		phone = phone.text
		
		if mobile:
			mobile = mobile.text
			phone = phone + ', ' + mobile
		
		if contact_person:
			contact_person = re.sub(r'^Key Pax: ', '',contact_person.text)
			contact_person = contact_person.replace('Key Pax: ', '')
		else:
			contact_person = '-'

		writerobj.writerow([company_name, address, phone, industry, sub_industry, contact_person])


url = "http://www.rajasthanindustries.org/ViewCompanyProfile.aspx?id=379&typet=alpha"
rajindus(url)
csv_file.close()

