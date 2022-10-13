import requests
from bs4 import BeautifulSoup
import json
import time 
import numpy as np
from support_functions import scrape_doc_info, get_documents_link, get_last_page_no
from htlm_keys_tags import tag_list, key_list
# Import the library
import argparse


# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--year', type=int, required=True)
# Parse the argument
args = parser.parse_args()
# Print "Hello" + the user input argument


article_no = 0
all_data_dict = {}
year = args.year
stop_year = year + 1

page_no = 1
response = requests.get(f'https://www.cia.gov/readingroom/search/site?page={page_no}&f%5B0%5D=dm_field_release_date%3A%5B{year}-01-01T00%3A00%3A00Z%20TO%20{year+1}-01-01T00%3A00%3A00Z%5D')
soup = BeautifulSoup(response.text, 'html.parser')
last_page = get_last_page_no(soup)

while page_no <= last_page:
    # get html 
    response = requests.get(f'https://www.cia.gov/readingroom/search/site?page={page_no}&f%5B0%5D=dm_field_release_date%3A%5B{year}-01-01T00%3A00%3A00Z%20TO%20{year+1}-01-01T00%3A00%3A00Z%5D')
    soup = BeautifulSoup(response.text, 'html.parser')
    link_list = get_documents_link(soup)


    for link in link_list:
        key = (str(year) + "-" + str(article_no))
        all_data_dict[key] = scrape_doc_info(link, tag_list, key_list)
        article_no +=1
    time.sleep(np.random.uniform(0, 2, 1)[0])
    print(page_no)
    page_no += 1  


with open(f'./data_{year}.json', "w") as outfile:
    json.dump(all_data_dict, outfile, indent=4, sort_keys=False)