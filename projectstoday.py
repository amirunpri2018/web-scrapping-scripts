# Script for retriving companies information from https://www.projectstoday.com/Directory/

import urllib.parse, urllib.error, urllib.request
import ssl
from bs4 import BeautifulSoup
import csv
import sys
import time
from selenium import webdriver
from termcolor import colored

categories = ["Machine Tools", "Mining", "Miscellaneous Manufacturing", "Packg. Material", "Paints, Dyestuff & Varnishes",
              "Paper & Paper Products", "Petrochemicals", "Textiles", "Petroleum Products", "Pipelines", "Plastics-Products",
              "Rubber & Products", "Wires & Cables"]

# to avoid ssl certificate issue
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

company_url = []
csv_file = open('projectstoday.csv', 'a')
writerobj = csv.writer(csv_file)
writerobj.writerow(['Company', 'Contact Person', 'Phone', 'Email'])


def parse_detail(link):
    txt = 'Fetching company link ' + link
    print(colored(txt, 'yellow'))
    html = urllib.request.urlopen(link, context=ctx)
    soup = BeautifulSoup(html, 'html.parser')
    company_name = soup.find('div', {'class': 'companydetailstitle'})
    try:
        company_name = company_name.text.strip()
    except:
        print(colored('Unknown Error', 'red'))
        return None

    txt = 'collecting data for ' + company_name
    print(colored(txt, 'green'))

    contact_title = soup.find_all('div', {'class': 'contacttitle'})
    for contact in contact_title:
        details = contact.parent

        if contact.text == 'Contact Person:':
            print('Found contact person details')
            all_person = details.find_all('div', {'class': 'contactpersonpadding'})

            for person in all_person:
                name = person.select('p')[0].text
                email = person.find(text='Email :')
                if email:
                    email = email.parent.parent.text.replace('Email :', '')
                mobile = person.find(text='Direct No :')
                if mobile:
                    mobile = mobile.parent.parent.text.replace('Direct No :', '')

                if email or mobile:
                    writerobj.writerow([company_name, name, email, mobile])
                    print(name, email, mobile)

        elif contact.text == 'Head Quarter':
            print('Found Head Quarter details')

            email = details.find(text='Email :')
            if email:
                email = email.parent.parent.text.replace('Email :', '')
            phone = details.find(text='Tel:')
            if phone:
                phone = phone.parent.parent.text.replace('Tel:', '')

            if email or phone:
                writerobj.writerow([company_name, None, email, phone])
                print(email, phone)

        elif contact.text == 'Branch':
            print('Found Branch details')

            email = details.find(text='Email :')
            if email:
                email = email.parent.parent.text.replace('Email :', '')
            phone = details.find(text='Tel:')
            if phone:
                phone = phone.parent.parent.text.replace('Tel:', '')

            if email or phone:
                writerobj.writerow([company_name, None, email, phone])
                print(email, phone)

        elif contact.text == 'Corporate':
            print('Found Corporate details')
            email = details.find(text='Email :')
            if email:
                email = email.parent.parent.text.replace('Email :', '')
            phone = details.find(text='Tel:')
            if phone:
                phone = phone.parent.parent.text.replace('Tel:', '')

            if email or phone:
                writerobj.writerow([company_name, None, email, phone])
                print(email, phone)
        else:
            continue


def parse_detail_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    companies = soup.find_all('div', {'class': 'ftcompanyname'})
    for company in companies:
        anchor = company.find('a')
        link = 'https://www.projectstoday.com' + anchor.get('href')
        company_url.append(link)

# Using selenium to retrive dyanamic content
def dyanamic_parsing(url):
    browser = webdriver.Chrome(executable_path='/home/graven/Desktop/chromedriver')
    print('Opening browser for url: ', url)
    browser.get(url)

    html_source = browser.page_source
    total_pages = browser.find_element_by_id('ContentPlaceHolder1_PFCompany1_lbldwnPageCnt')
    parse_detail_link(html_source)

    for i in range(int(total_pages.text)-1):
        print('clicking on page no.', i+2)
        browser.find_element_by_id("ContentPlaceHolder1_PFCompany1_imgdwnBtnNext").click()
        time.sleep(10) # waits 10 seconds to load content
        html_source = browser.page_source
        parse_detail_link(html_source)
    print('Quitting Browser')
    browser.quit()
    for url in company_url:
        parse_detail(url)

    del company_url[:]


def get_subcategory_link(url, category):
    html = urllib.request.urlopen(url, context=ctx)
    soup = BeautifulSoup(html, 'html.parser')

    tags = soup.find_all('div', {'class': 'widthfullsize'})

    for tag in tags:
        anchor = tag.find('a', id='lnkActivity')
        link = 'https://www.projectstoday.com' + anchor.get('href')
        txt = 'Fetching data for Sub-Category: ' + anchor.text.strip() + ' Category: ' + category
        print(colored(txt, 'blue'))
        dyanamic_parsing(link)


link = 'https://www.projectstoday.com/Directory/'

html = urllib.request.urlopen(link, context=ctx)
soup = BeautifulSoup(html, 'html.parser')

categories_tag = soup.find_all('div', {'class': 'widthfullsize'})

for tag in categories_tag:
    anchor = tag.find('a', id='lnkActivity1')

    if anchor.text.strip() in categories:
        category_url = 'https://www.projectstoday.com' + anchor.get('href')
        msg = 'Fetching Sub-Category links of ' + anchor.text.strip()
        print(colored(msg, 'cyan'))
        get_subcategory_link(category_url, anchor.text.strip())
