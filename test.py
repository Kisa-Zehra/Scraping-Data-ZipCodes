from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from multiprocessing import cpu_count, Pool
import pandas as pd
import logging
import time

logger = logging.getLogger()

zip_codes = pd.read_csv("zipcode.csv")


# def generate_urls():
#     all_urls = []
#     for x,row in zip_codes.iterrows():
#       dealers_url = "https://www.cargurus.com/Cars/dl.action?entityId=&address={}+{}+{}&latitude={}&longitude={}&distance=100".format(row['city_slug'],row['state_id'],row['zip'],row['lat'],row['log'])
        
#       all_urls.append(dealers_url)
#     return all_urls


def get_driver():
  logger.info("Initializing driver creation")
  # urls = generate_urls(generate_urls())
  
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  
  driver = webdriver.Chrome(options = chrome_options)

  driver.get(url)

  logger.info("Completed driver creation")
  
  return driver

def get_dealer(driver):

  logger.info("Getting all the dealers")
  # urls = generate_urls(generate_urls())
  
  
  DEALER_DIV_CLASS = 'blade'

  driver.get(url)
  
  dealer = driver.find_elements(By.CLASS_NAME,DEALER_DIV_CLASS)

  logger.info("Completed all dealers")

  return dealer


def parse_dealer(dealer):

  logger.info("Getting dealers details")
  
  name_tag = dealer.find_element(By.CLASS_NAME, 'details')
  dealer_name = name_tag.text
  
  url_tag = dealer.find_element(By.TAG_NAME,'a')
  url = url_tag.get_attribute('href')

  address = dealer.find_element(By.CLASS_NAME, 'address').text

  logger.info("Complete dealers details")

  return{
    'dealer name': dealer_name,
    'url': url,
    'address' : address
  }


if __name__=="__main__":

  start_time = time.time()

  
  
  # for ind,row in zip_codes.iterrows():
  #   url = f"""https://www.cargurus.com/Cars/dl.action?entityId=&address={row['city_slug']}+{row['state_id']}+{row['zip']}&latitude={row['lat']}&longitude={row['log']}&distance=100"""

  
  
  # url = "https://www.cargurus.com/Cars/dl.action?entityId=&address=castaner+PR+631&latitude=18.1856&longitude=-66.8333&distance=100"



  print('\n\t Total time taken:', time.time()-start_time)
  
  print("Creating driver")
  driver = get_driver()


  # print("multi process start")
  # url = generate_urls()
  # p = Pool(20)
  # result = p.map(parse_dealer, url)
  # p.close()
  # p.join()
  # print("multi process over")


  print(1)
  all_urls = []
  for x,row in zip_codes.iterrows():
    dealers_url = "https://www.cargurus.com/Cars/dl.action?entityId=&address={}+{}+{}&latitude={}&longitude={}&distance=100".format(row['city_slug'],row['state_id'],row['zip'],row['lat'],row['log'])
        
    url = all_urls.append(dealers_url)

  p = Pool(20)
  result = p.map(parse_dealer, url)
  p.close()
  p.join()
  print(2)
  print(url)
  print(3)
  

  print("Fetching dealer")
  dealers = get_dealer(driver)
  print("finished fetching dealer")

  print(f'Found {len(dealers)} dealer')
  print("finished length dealer")
  

  print("Parsing dealers")
  dealer_data =[parse_dealer(dealer) for dealer in dealers]
  print(dealer_data)
  print("finished dealer details")

  
  print("Creating CSV of all dealer details")
  print('Save the data in CSV')
  dealers_df = pd.DataFrame(dealer_data)
  dealers_df[['Dealer_id']] = dealers_df['url'].str.split('-sp', expand=True)
  print("new column")
  print(dealers_df)
  dealers_df.to_csv('dealer.csv', index=None)

  
