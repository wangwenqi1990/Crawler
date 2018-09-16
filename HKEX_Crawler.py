from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from bs4 import BeautifulSoup
#import re
import urllib2
import csv

def save_html(data, path):
	f = open(path, 'wb')
	f.write(data.encode('utf-8'))
	f.close()

def request_process(txtStockCode, year, month, day):
    # processing saving path and timer
    start = time.time()
    filename = txtStockCode +'_'+year+month+day+'.html'
    path = os.getcwd() + '/' + filename
    
    # read website
    driver = webdriver.Chrome()
    driver.get("http://www.hkexnews.hk/sdw/search/searchsdw.aspx")

    # select stock
    driver.find_element_by_name("txtStockCode").send_keys(txtStockCode)
    # select Year: 0 and 1 represents 2018 and 2017 respectively
    driver.find_element_by_id('ddlShareholdingYear').find_elements_by_tag_name('option')[2018-int(year)].click()
    # select Month: 0-11 represents Jan to Dec
    driver.find_element_by_id('ddlShareholdingMonth').find_elements_by_tag_name('option')[int(month)-1].click()
    # select Day: 0-30 represents 1-31
    driver.find_element_by_id('ddlShareholdingDay').find_elements_by_tag_name('option')[int(day)-1].click()

    # send request -> save file -> close browser 
    elem = driver.find_element_by_name("txtStockCode")
    elem.send_keys(Keys.RETURN)
    data = driver.page_source;
    save_html(data, path)
    driver.close()

    # Time the code
    end = time.time()
    print 'processing['+ filename + '] takes time: ' + str(end-start)

def save2csv(txtStockCode, year, month, day):
    start = time.time()
    url = 'file://'+os.getcwd() + '/' + txtStockCode +'_'+year+month+day+'.html'
    html = urllib2.urlopen(url)
    bsObj = BeautifulSoup(html, 'lxml')                         
    csvname = txtStockCode +'_'+year+month+day+'.csv'                             

    with open(csvname, 'wb') as  csvfile:
        writer = csv.writer(csvfile)
        # write query info and display info
        writer.writerow(['Query:',year+month+day, txtStockCode])
        stockname = str(bsObj.findAll(bgcolor="#F5F5F5")[1].get_text().split('\n')[17].lstrip())
        date= str(bsObj.findAll(bgcolor="#F5F5F5")[0].get_text().split('\n')[9].lstrip())
        writer.writerow(['Display:', stockname, date])
        writer.writerow([''])
        
        # write table 1
        writer.writerow(['', 'Shareholding in CCASS', 'Number of Participants', \
                         '% of the total number of Issued Shares/Warrants/Units'])
        table1 = bsObj.findAll(class_="mobilezoom")
        writer.writerow(['Market Intermediaries']+\
                        [str(table1[i].get_text().replace('\n', '').replace(' ', '')) for i in (2 ,3 ,4 )])
        writer.writerow(['Consenting Investor Participants']+ \
                        [str(table1[i].get_text().replace('\n', '').replace(' ', '')) for i in (5 ,6 ,7 )])
        writer.writerow(['Non-consenting Investor Participants']+ \
                        [str(table1[i].get_text().replace('\n', '').replace(' ', '')) for i in (8 ,9 ,10)])    
        writer.writerow(['Total']+ \
                        [str(table1[i].get_text().replace('\n', '').replace(' ', '')) for i in (11,12,13)])  
        writer.writerow(['Total number of Issued Shares/Warrants/Units (last updated figure)']+ \
                         [str(table1[14].get_text().replace('\n', '').replace(' ', ''))])
        writer.writerow([''])
    
        # write table 2
        table2 = bsObj.findAll(True, {'class':["row0", "row1"]})
        writer.writerow(['Participant ID', 'Name of CCASS Participant (* for Consenting Investor Participants)',\
                         'Address', 'Shareholding', '% of the total number of Issued Shares/Warrants/Units'])
        for i in range(len(table2)):
            writer.writerow([table2[i].text.split('\n')[j].lstrip() for j in (2,5,8,11,14)])
        end = time.time()
        print 'processing['+ csvname + '] takes time: ' + str(end-start)
    
# input parameters
txtStockCode = '00005'
year = '2018'
month= '07'
day  = '02'
request_process(txtStockCode, year, month, day)
save2csv(txtStockCode, year, month, day)




