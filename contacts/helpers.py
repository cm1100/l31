import json
import selenium.webdriver as webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import re
import phonenumbers
import os
from webdriver_manager.chrome import ChromeDriverManager

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-setuid-sandbox")

chromeOptions.add_argument("--remote-debugging-port=9222")  # this

chromeOptions.add_argument("--disable-dev-shm-using")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-gpu")
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument(r"user-data-dir=.\cookies\\test")


def get_results(college_name):
    driver = webdriver.PhantomJS()
    search_term=f"{college_name} placement officer"
    url = f"https://www.google.com/search?q={search_term}"
    base_url ="google"

    driver.get(url)

    links = driver.find_elements_by_xpath("//a")

    results =[]
    num=0
    for link in links:
        href = link.get_attribute("href")
        if href != None:
            if base_url  not in str(href) and "linkedin" not in str(href):


                results.append(href)
                num+=1
                if num==2:
                    break

    # new code start

    base_urls = ""
    for r in results:
        m = r.split("/")
        base_urls += m[0] + "//" + m[2]
        break

    results_new = []
    for r in results:
        driver.get(r)

        content = BeautifulSoup(driver.page_source, 'lxml')
        contact = content.find('a', text=re.compile('contact', re.IGNORECASE))
        if contact:

            if "https" in contact['href']:
                if base_urls in contact["href"]:
                    results_new.append(contact['href'])
            else:
                if contact["href"].split()[0] == "/":
                    results_new.append(base_urls + contact['href'])
                else:
                    results_new.append(base_urls + "/" + contact['href'])
    results += results_new

    # new code end


    driver.quit()
    return results


def get_phone_emails(links):
    phone_list=[]
    email_list=[]

    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chromeOptions)

    for link in set(links):
        url = link


        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        text = soup.text

        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
        email_list+=emails


        try:
            rregex_main = r"\+?\d[\d -]{8,12}\d\d"
            phone_list += re.findall(rregex_main, text)
        except:
            pass

        try:
            regex_2_try = r"(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})"

            def get_num(ree):
                nums = []
                for x in re.findall(ree, text):
                    m = ''.join(x)
                    nums.append(m)
                # print(f"nums:{nums}")
                return nums

            phone_list += get_num(regex_2_try)
        except:
            pass

    phone_list_new = []
    for x in range(len(phone_list)):
        phone_list_new.append(phonenumbers.parse(phone_list[x], region='IN'))

    phone_list_new_2 = []
    for x in range(len(phone_list)):
        if phonenumbers.is_valid_number(phone_list_new[x]):
            phone_list_new_2.append(phone_list[x])





    driver.quit()
    return (set(email_list),set(phone_list_new_2))


