import numpy as np
import sys
from libgen_api import LibgenSearch
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import urllib.request as urllib2
from fake_useragent import UserAgent
import requests
import os
from tqdm import tqdm

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tabulate import tabulate

from rich import box
from rich.table import Table
from rich.console import Console
from time import sleep


#dont use this code for automated testing as it may hammer the server -vivek (author).

#EMAIL Constants
SERVER_ADDRESS = "smtp.mail.yahoo.com"
SERVER_PORT = 587
SENDER_EMAIL_ADDRESS = "bookkeeper61611@yahoo.com"
SENDER_APP_EMAIL_PASSWORD = "jlazkhixseoxzppo"
EMAIL_SUBJECT = "From bookkeeper : "

def dlinker(link):
    req = Request(link)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page,features="lxml")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    return links[0]

def downloadBook(url: str, fname: str):
	fname=fname+".pdf"
	headers = {'User-Agent': 'Mozilla/5.0'}
	resp = requests.get(url, stream=True, headers=headers)
	total = int(resp.headers.get('content-length', 0))
	with open(fname, 'wb') as file, tqdm(
		desc=fname,
		total=total,
		unit='iB',
		unit_scale=True,
		unit_divisor=1024,
	) as bar:
		for data in resp.iter_content(chunk_size=1024):
			size = file.write(data)
			bar.update(size)

def portBookToKindle(book_name):
	try:
		print("Sending book: "+ book_name +"to kindle");
		fromaddr=SENDER_EMAIL_ADDRESS
		toaddr=input("Enter your email address to receive the downloaded e-book as an attachment : ");
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		filename = book_name+".pdf";
		subject = EMAIL_SUBJECT + filename
		msg['Subject'] = subject
		attachment = open(os.getcwd() + "/" +filename, "rb")
		p = MIMEBase('application', 'octet-stream')
		p.set_payload((attachment).read())
		encoders.encode_base64(p)
		p.add_header('Content-Disposition', "attachment",filename=filename)
		msg.attach(p)
		s = smtplib.SMTP(SERVER_ADDRESS, SERVER_PORT)
		s.starttls()
		#password=input("Please enter your email password || incase of two factor auth use generated app password from google");
		print("Sending email with attachment....")
		s.login(fromaddr, SENDER_APP_EMAIL_PASSWORD);
		text = msg.as_string()
		if s.sendmail(fromaddr, toaddr, text):
			print("Email sent successfully!")
	except Exception as e:
		print("Failed to send email...try again!",e)
	finally:
		s.quit()


s = LibgenSearch()
text=sys.argv[1]
title_filters = {"Extension": "pdf","Language": "English"}
results = s.search_title_filtered(text,title_filters,exact_match=True);
i=1;
links=[];

#Table headers
headers = [
"Index",
"Author",
"Title",
"Size",
"File Extension"
]

search_result_list = []
temp_list = []


table = Table("Index",title="-: Books found for the given keyword :-",box=box.DOUBLE,show_lines=True,highlight=True)
#table.add_column("Index", justify="center", style="bright_yellow", no_wrap=True)
table.add_column("Author", justify="left", style="red", no_wrap=False)
table.add_column("Title", justify="left", style="green", no_wrap=True)
table.add_column("File Size", justify="left", style="blue", no_wrap=True)
table.add_column("File Extension", justify="left", style="magenta", no_wrap=True)

if len(results) > 0:

	for res in results:
	    #print(i,") ",res['Author'],"||",res['Title'],"||",res['Size'],"||",res['Extension']);
	    temp_list.append(str(i))
	    temp_list.append(res['Author'])
	    temp_list.append(res['Title'])
	    temp_list.append(res['Size'])
	    temp_list.append(res['Extension'])
	    search_result_list.append(temp_list)

	    table.add_row(str(i),res['Author'],res['Title'],res['Size'],res['Extension'])

	    temp_list = []

	    #Appending book urls to links list 
	    links.append(dlinker(res['Mirror_1']));
	    i+=1;


	#print(tabulate(search_result_list,headers, tablefmt="fancy_grid"))

	console = Console()
	console.print(table)

	book_idx=input("EnterBookIndex: ");
	book_idx=int(book_idx);
	book_name=results[book_idx-1]['Title'];
	downloadBook(links[book_idx-1],book_name);
	portBookToKindle(book_name);

else:
	print("No matchings found for given keyword!!")
