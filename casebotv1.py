#from https://preethamdpg.medium.com/running-selenium-webdriver-with-python-on-an-aws-ec2-instance-be9780c97d47
#Successfully build function to retrieve case information from portal for a list of cases.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import pandas as pd
import xlrd, xlwt
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)






case_list = []




print("  Welcome to CaseBot. ", "\n")

list_or_file = input("Will you be using a list of cases or an xlsx file? Enter L for list or F for file? ")

if list_or_file == "L":
    case_list = [input("Enter case numbers separated by commas: ")]
elif list_or_file == "F":
    file_name = input("Enter file name including the xlsx extension suffix: ")
    file = pd.read_excel(file_name)
    row_end = input("Please enter the row in column A where the data ends: ")
    file_df = pd.DataFrame(file)
    def create_list():
        master_case_list = []
        name_of_file =  file_name
        data = pd.read_excel(file_name)
        myRange = data
        master_case_list = myRange
        case_list = master_case_list
        print('Data on selected sheet :' , '\n,', case_list)
    create_list()
    print("Searching for cases in the web portal, please wait. ")

else:
    print("Not understood, please run script again!")


date_results = []
type_results = []
room_results = []
status_results =[]


#remove html tags

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)










def search_bot(i):
        driver.get("https://web6.seattle.gov/courts/ECFPortal/default.aspx")
        driver.find_element(By.XPATH, "//li[4]/a/span/span/span").click()
        time.sleep(4)
        driver.find_element(By.XPATH, "//div[@id='ContentPlaceHolder1_CaseInfo1_CaseSearch1_pnlSubmit']/input").click()
        driver.find_element(By.XPATH, "//div[2]/div/div[3]/div/input").send_keys(str(i))
        driver.find_element(By.XPATH, "//div[2]/div/div[3]/div/input[2]").click()
        driver.find_element(By.XPATH, "//div[2]/div/ul/li[3]/a/span/span/span").click()
        time.sleep(6)   
        date = driver.find_element(By.XPATH, "//div[2]/div/div/table/tbody/tr/td").get_attribute("outerHTML")
        room = driver.find_element(By.XPATH, "//div[2]/div/div/table/tbody/tr/td[3]").get_attribute("outerHTML")
        statush = driver.find_element(By.XPATH, "//div[2]/div/div/table/tbody/tr/td[4]").get_attribute("outerHTML")
        hearing_type = driver.find_element(By.XPATH, "//div[2]/div/div/table/tbody/tr/td[2]").get_attribute("outerHTML")
        date_results.append(remove_html_tags(date))
        type_results.append(remove_html_tags(hearing_type))
        room_results.append(remove_html_tags(room))
        status_results.append(remove_html_tags(statush))


def add_values():
        dates_df2 = pd.DataFrame(index=None)
        dates_df2['Hearing Date'] = date_results
        dates_df2['Case Number'] = case_list
        dates_df2['Hearing Type'] = type_results
        dates_df2['Room Number'] = room_results
        dates_df2['Case Status'] = status_results
        dates_df2 = pd.DataFrame()
        dates_df2['Case Number'] = case_list
        dates_df2['Hearing Date'] = date_results
        dates_df2['Hearing Type'] = type_results
        dates_df2['Room Number'] = room_results
        dates_df2['Hearing Status'] = status_results
        print(dates_df2)
        dates_df2.to_csv("results.csv")




for i in case_list:
    search_bot(i)
    add_values()






#element_text = driver.page_source
#print(element_text)
