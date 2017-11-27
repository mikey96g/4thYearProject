# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

sentData
import requests

from bs4 import BeautifulSoup
page = requests.get("http://www.coindesk.com/?s=Bitcoin")

url = "https://www.coindesk.com/?s=bitcoin"
soup=BeautifulSoup(page.content, 'html.parser')

sentData = soup.find_all(class_="desc")
print(sentData)

#time = soup.find_all(class_ = )