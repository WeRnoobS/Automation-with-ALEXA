import re
from bs4 import BeautifulSoup
import requests
import json
import httplib2
import urllib.request
from selenium import webdriver
import argparse

url = 'https://jntuaresults.ac.in/'

try:
    src = requests.get('https://jntuaresults.ac.in/').text
except:
    print('no internet')
    exit()

soup = BeautifulSoup(src, 'lxml')

table = soup.find('table', {'class': 'ui table segment'})


def getRes_a(value1, value2):
    geturl = ""
    year=value2.split(" ")[1]
    month=value2.split(" ")[0]
    for row in soup.findAll("a", href=True):
        if value1 in row.text:
            # print(row.text)
            h = row['href']
            geturl = f'{url}{h}'
            print(f'{row.text} : {geturl}')
            if month in row.text:
                if  year in row.text:
                    return geturl
                else:
                    return "result not found or has been deleted by Admin"




if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('val1', help='val 1')
    p.add_argument('val2', help='val 2')
    args = p.parse_args()

    l=getRes_a(args.val1, args.val2)
    print(l)
    if l!=None: 
        rollno = '163G1A0548'
        browser = webdriver.Chrome("E:\Final_year_projects\Client_api\Executing\chromedriver.exe")
        print(l)
        browser.get(l)
        field = browser.find_element_by_xpath(
            '/html/body/div/div[1]/div/div/center/table/tbody/tr/th/center/input[1]')
        btn = browser.find_element_by_xpath(
            '/html/body/div/div[1]/div/div/center/table/tbody/tr/th/center/input[2]')
        field.send_keys(rollno)
        btn.click()
    else        :         
        browser = webdriver.Chrome("E:\Final_year_projects\Client_api\Executing\chromedriver.exe")
        browser.get("https://alexautomation.herokuapp.com/")
        



'''
    usage : python Rantest1.py "B.Tech IV Year I Semester (R15)" "Nov/Dec 2019"
    
'''