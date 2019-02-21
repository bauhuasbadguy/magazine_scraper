# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 00:05:37 2018

@author: stuart
"""

#download NGC magazine automatically

from bs4 import BeautifulSoup
import requests
import re
import shutil

import time


#homepage_url = 'https://archive.org/details/ngc_magazine'

save_folder = '/home/stuart/Documents/Python_scripts/NGC_magazine/NGC_archive/'


homepage_url = 'https://archive.org/details/ngc_magazine?sort=-date'

html_doc = requests.get(homepage_url).text

soup = BeautifulSoup(html_doc, 'html.parser')

#iterate through the list of issues on the main page
for el in soup.findAll('div', 'item-ttl')[16:]:
    
    target_url1 = 'https://archive.org' + el.find('a')['href']
    
    layer1_html = requests.get(target_url1).text
    
    soup2 = BeautifulSoup(layer1_html, 'html.parser')
    
    table_elements = soup2.findAll('div', 'format-group')
    try:
        issue_number = soup2.findAll('h1')[0].text.lstrip().rstrip().replace(' ','-')#('div', 'thats-left')
        
        print(issue_number)
    except:
        issue_number = None
        print('COULD NOT SCRAPE ISSUE')
    
    #check there is an issue to scrape
    if issue_number != None:
        #iterate through table elements to find the one that corresponds to the
        #one we want
        for tab_el in table_elements:
            
            pdf_url = tab_el.find('a')['href']
            
            #get the name of the table element we are looking at
            title = tab_el.find('a', 'format-summary download-pill').text
            
            #clean the name of this table element to read it
            clean_title = re.sub('[ ]+', ' ', title).lstrip().rstrip()
    
            start_download = time.time()
            
            #if we have the table element corresponding to the raw pdf
            if clean_title == 'PDF download':
                
                out_filename = save_folder + issue_number + '.pdf'           
                
                pdf_response = requests.get('https://archive.org' + pdf_url, stream=True)
                
                with open(out_filename, 'wb') as out_file:
                    shutil.copyfileobj(pdf_response.raw, out_file)
                del pdf_response
                
                download_time = time.time() - start_download
                
                print('This issue took %s minutes'%str(download_time/60))
    
        