import urllib.request, urllib.parse, urllib.error
import ssl
import re
import csv
from bs4 import BeautifulSoup

# to avoid ssl certificate issue
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
pincode_pattern = re.compile('\d\d\d\d\d\d')

csv_file = open('company_detail.csv', 'a')
writerobj = csv.writer(csv_file)

def get_detail(url):
	markup = urllib.request.urlopen(url, context=ctx)
	websoup = BeautifulSoup(markup, 'html.parser')
	address_tag = websoup.find('font', text="Address")
	
	# to get the text without tag after font tag 
	add1 = address_tag.next_sibling

	# removing unnecessary character and spaces
	add1 = re.sub(r'^ - ', '', add1).split()

	# to get the text without tag after br tag 
	add2 = address_tag.findNext('br').next_sibling
	pincode = pincode_pattern.findall(add2)
	address = ' '.join(add1) + ' Bhilwara Rajasthan, ' + pincode[0]

	phone_tag = websoup.find('div', {'class':"detail-line"})
	phone = phone_tag.text.split('\n')[0].strip()
	
	return address, phone


urls = ['https://www.fundoodata.com/companies-in/bhilwara-l61?&pageno=1&tot_rows=66&total_results=66&no_of_offices=0',
		'https://www.fundoodata.com/companies-in/bhilwara-l61?&pageno=2&tot_rows=66&total_results=66&no_of_offices=0',
		'https://www.fundoodata.com/companies-in/bhilwara-l61?&pageno=3&tot_rows=66&total_results=66&no_of_offices=0',
		'https://www.fundoodata.com/companies-in/bhilwara-l61?&pageno=4&tot_rows=66&total_results=66&no_of_offices=0'
		]

for url in urls:		

	html = urllib.request.urlopen(url, context=ctx)
	soup = BeautifulSoup(html, 'html.parser')

	tags = soup.find_all('div', {'class':"search-result-left"})

	for tag in tags:
		if tag.find('table'):
			company = tag.select('div > a')[0]
			company_name = company.text
			detail_link = 'https://www.fundoodata.com/' + company.get('href')
			address, phone = get_detail(detail_link)
			industry = tag.find(text='Industry')
			sub_industry = tag.find(text='Sub Industry')
			contact_person = '-'

			if industry:			
				industry = industry.findNext('td')
				industry = industry.text.split(' : ')[1]
			else:
				industry = '-'

			if sub_industry:
				sub_industry = sub_industry.findNext('td')
				sub_industry = sub_industry.text.split(' : ')[1]
			else:
				sub_industry = '-'

			writerobj.writerow([company_name, address, phone.replace(' ', '/'), industry, sub_industry, contact_person])


			print(company_name, address, phone.replace(' ', '/'), industry, sub_industry, contact_person)

		
csv_file.close()
		

