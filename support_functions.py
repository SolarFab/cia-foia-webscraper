from inspect import Attribute
import requests
from bs4 import BeautifulSoup
import json
import time 
import numpy as np


def get_last_page_no(soup):
    """
    This function returns the last page number with documents.
    The last page number can be extracted from link which is saved in the selector with title 'Got to last page'
    
    """
    last_page = soup.find('a', attrs={'title': 'Go to last page'}) # find the url saved under the tag "a" with title "Go to last page"
    link_last_page = last_page['href'] # assigns the link of last page to variable

    first_letter = link_last_page.index('=') + 1 #the page number starts after the first "=" in the link
    last_letter = link_last_page.index("&") #the page number ends before the first "&" in the link

    last_page_no = int(link_last_page[first_letter:last_letter]) #assigns the last page no to a variable

    return(last_page_no)



def get_documents_link(soup):
    """
    This function returns a list of all links at webpage which link to the final documents
    As input it requires a beautiful soup object
    """
    link_list = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('https://www.cia.gov/readingroom/document/'):
            link_list.append(link['href'])
    return(link_list)


def scrape_doc_info(link,tag_list, key_list):
    
    i = 0
    scrapped_data_dict = {}
    response_document = requests.get(link)
    soup_document = BeautifulSoup(response_document.text,'html.parser')
   

    for key in key_list:
        # finds the data
        try:
            data = soup_document.find('div', attrs={'class':tag_list[i]})
            data_text = data.find('div', attrs={'class':"field-item even"})
            
            # all data are stored as text, but "document URl","Document Header","file-link" which are stored differently
            # therefore the data of these tags will be searched differently
        
            if key == "Document URL":  
                scrapped_data_dict[key] = link

            elif key == "Document Header":
                header = soup_document.find('h1', attrs={'class':"documentFirstHeading"})
                scrapped_data_dict['Document Header'] = header.text

            elif key == "File Link":
                scrapped_data_dict[key] = data_text.a['href']
                i = i + 1
            else:
                scrapped_data_dict[key] = data_text.text
                i = i + 1
        except AttributeError:
            continue
        
    return(scrapped_data_dict)