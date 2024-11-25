import argparse
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
from rich.progress import track
from time import sleep

# Email Constants
SERVER_ADDRESS = "smtp.mail.yahoo.com"
SERVER_PORT = 587
SENDER_EMAIL_ADDRESS = "bookkeeper61611@yahoo.com"
SENDER_APP_EMAIL_PASSWORD = "jlazkhixseoxzppo"
EMAIL_SUBJECT = "From bookkeeper : "

def dlinker(link):
    try:
        req = Request(link)
        html_page = urlopen(req)
        soup = BeautifulSoup(html_page, features="lxml")
        links = [link.get('href') for link in soup.findAll('a')]
        return links[0] if links else None
    except Exception as e:
        print(f"Error in dlinker: {e}")
        return None

def downloadBook(url: str, fname: str):
    fname = fname + ".pdf"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, stream=True, headers=headers)
        resp.raise_for_status()
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
        print(f"Successfully downloaded: {fname}")
    except requests.RequestException as e:
        print(f"Error downloading book: {e}")

def portBookToKindle(book_name):
    try:
        print(f"Sending book: {book_name} to kindle")
        fromaddr = SENDER_EMAIL_ADDRESS
        toaddr = input("Enter your email address to receive the downloaded e-book as an attachment: ")
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        filename = f"{book_name}.pdf"
        subject = EMAIL_SUBJECT + filename
        msg['Subject'] = subject
        
        with open(os.path.join(os.getcwd(), filename), "rb") as attachment:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment", filename=filename)
            msg.attach(p)
        
        with smtplib.SMTP(SERVER_ADDRESS, SERVER_PORT) as s:
            s.starttls()
            print("Sending email with attachment....")
            s.login(fromaddr, SENDER_APP_EMAIL_PASSWORD)
            text = msg.as_string()
            s.sendmail(fromaddr, toaddr, text)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def search_and_download(search_term):
    s = LibgenSearch()
    title_filters = {"Extension": "pdf", "Language": "English"}
    try:
        results = s.search_title_filtered(search_term, title_filters, exact_match=True)
    except Exception as e:
        print(f"Not able to find any books with this title: {e}")
        return

    if not results:
        print("No matching books found for the given keyword!")
        return

    table = Table(title="-: Books found for the given keyword :-", box=box.DOUBLE, show_lines=True, highlight=True)
    table.add_column("Index", justify="center", style="bright_yellow", no_wrap=True)
    table.add_column("Author", justify="left", style="red", no_wrap=False)
    table.add_column("Title", justify="left", style="green", no_wrap=True)
    table.add_column("File Size", justify="left", style="blue", no_wrap=True)
    table.add_column("File Extension", justify="left", style="magenta", no_wrap=True)

    links = []
    for i, res in enumerate(results, 1):
        table.add_row(str(i), res['Author'], res['Title'], res['Size'], res['Extension'])
        link = dlinker(res['Mirror_1'])
        if link:
            links.append(link)

    console = Console()
    console.print(table)

    while True:
        try:
            book_idx = int(input("Enter Book Index (or 0 to exit): "))
            if book_idx == 0:
                return
            if 1 <= book_idx <= len(results):
                break
            print("Invalid index. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    book_name = results[book_idx-1]['Title']
    downloadBook(links[book_idx-1], book_name)
    
    if input("Do you want to send this book to Kindle? (y/n): ").lower() == 'y':
        portBookToKindle(book_name)

def main():
    parser = argparse.ArgumentParser(description="Search and download books from LibGen.")
    parser.add_argument("search_term", nargs='+', help="The book title to search for")
    args = parser.parse_args()

    search_term = ' '.join(args.search_term)
    search_and_download(search_term)

if __name__ == "__main__":
    main()
