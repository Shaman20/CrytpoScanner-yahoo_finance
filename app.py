# Import required libraries
import csv
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import pdfkit

url = 'https://yfapi.net/v1/finance/trending/US'
querystring = {"symbols":"AAPL,BTC-USD,EURUSD=X"}

headers = {
    'x-api-key': "RGVrpn12Qf2gtm3cytKrs5L1zn9hNYEb6B19A61M"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
        
# Empty List
name = []
price = []
change = []
change2 = []
market_cap = []
volume = []

# To fetch data from all pages in the website
for i in range(1,11):
    # To store website name
    website = 'https://finance.yahoo.com/cryptocurrencies/?count=25&offset=' + str(i)
    
    # Recieve response from website
    response = requests.get(website)
    # Soup Object
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Scraping Table
    results = soup.find('table', {'class' : 'W(100%)'}).find('tbody').find_all('tr')
    
    # Scraping data from single page
    for result in results:
        # Appending Values
        try:
            name.append(result.find(
                'a', {'class': 'Fw(600) C($linkColor)'}).get_text().strip())
        except:
            name.append('\n/a')

        try:
            price.append(result.find(
                'td', {'class': 'Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)'}).get_text())
        except:
            price.append('\n/a')
        
        try:
            change.append(result.find('td', {
            'class': 'Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)', 'aria-label': 'Change'}).get_text())
        except:
            change.append('\n/a')
        try:
            change2.append(result.find('td',{
            'class': 'Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)', 'aria-label': '% Change'}).get_text())
        except:
            change2.append('\n/a')
        
crypto_data = pd.DataFrame({'Coin' : name, 'Price' : price, 'Change' : change, 'Change_24hr' : change2})
print(pd.DataFrame(crypto_data))
#Genterate Excel
crypto_data.to_excel('crypto_news.xlsx', index=False)
crypto_data.to_csv('data.csv')

# Headers for JSON
dataForCsv = {'Coin' : name, 'Price' : price, 'Change' : change, 'Change_24hr' : change2} 

# Dumping python list of dictionary as json
stringData = json.dumps(dataForCsv)

# Putting JSON into csv
file = open('sample.csv', 'w')
writer = csv.writer(file)
writer.writerow(stringData)
file.close() 

# Stroing Python dictionary as json
with open('file.json', 'w') as dataFile:
    dataFile.write(stringData)
    dataFile.close()
                       

PATH = 'C:\Program Files (x86)\chromedriver.exe'

# Setting chromedriver path

browser = webdriver.Chrome(PATH)
# Navingating to desired page
browser.get('https://finance.yahoo.com/topic/crypto/')

ele = browser.find_element(By.ID,'yfin-usr-qry')

# Passing the query
ele.send_keys('Ethereum')
ele1 = browser.find_element(By.ID,'header-desktop-search-button')
# Click on button
ele1.click()

# Generating pdf 
pdfkit.from_url('https://finance.yahoo.com/quote/ETH-USD?p=ETH-USD&.tsrc=fin-srch', 'crypto_news.pdf')
