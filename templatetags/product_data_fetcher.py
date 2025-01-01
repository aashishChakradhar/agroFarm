import requests
from bs4 import BeautifulSoup
import re
import time

def get_product_data():
    url = "https://kalimatimarket.gov.np/lang/en"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tbody = soup.find('tbody')
        if tbody:
            vegdict = {}
            texts = [tag.get_text(strip=True) for tag in tbody.find_all('tr') if tag.get_text(strip=True)]

            for x in texts:
                item = x.split('Rs')
                new_text = re.sub(r'\((.*?)\)', r'-\1', item[0])
                t = re.sub(r'\s+', '-', new_text)

                if t not in vegdict:
                    vegdict[t] = {'name': '', 'min': '', 'max': '', 'avg': ''}

                vegdict[t]['name'] = item[0].strip() 
                vegdict[t]['min'] = item[1].strip() 
                vegdict[t]['max'] = item[2].strip() 
                vegdict[t]['avg'] = item[3].strip() 

            return vegdict
        else:
            return "ID not found"
    else:
        return (f"Failed to fetch the page. Status code: {response.status_code}")
