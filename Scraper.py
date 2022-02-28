from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from multiprocessing import cpu_count, Pool
import pandas as pd
# import threading
import logging
import time
import itertools

# import concurrent.futures

MAX_THREADS = 10

logger = logging.getLogger()

zip_codes = pd.read_csv("zipcode.csv")

# dealers_url = []

# for ind,row in zip_codes.iterrows():
#     url = f"""https://www.cargurus.com/Cars/dl.action?entityId=&address={row['city_slug']}+{row['state_id']}+{row['zip']}&latitude={row['lat']}&longitude={row['log']}&distance=100"""
#     dealers_url.append(url)

def generate_urls():
  limit = 5
  all_urls = []
  for x,row in itertools.islice(zip_codes.iterrows(), limit):
    dealers_url = "https://www.cargurus.com/Cars/dl.action?entityId=&address={}+{}+{}&latitude={}&longitude={}&distance=100".format(row['city_slug'],row['state_id'],row['zip'],row['lat'],row['log'])
    all_urls.append(dealers_url)
  return all_urls


# def get_dealer():
    

    #  for d in dealers_url:

    # return driver


def parse_dealer(url):
  print(url)
  print("____________________________________")

  logger.info("Initializing driver creation")

  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')

  driver = webdriver.Chrome(options=chrome_options)
  print("1")
  # for urls in url:
  driver.get(url)
  print("2")

  DEALER_DIV_CLASS = 'blade'

  dealer = driver.find_elements(By.CLASS_NAME, DEALER_DIV_CLASS)

  print('extracted dealers')

  name_tag = driver.find_element(By.CLASS_NAME,'details')
  dealer_name = name_tag.text

  print("extracted dealers name")
  
  url_tag = driver.find_element(By.TAG_NAME,'a')
  dealer_url = url_tag.get_attribute('href')

  print("extracted dealers url")

    # add_tag = dealer.find_element(By.TAG_NAME, 'span')
  address = driver.find_element(By.CLASS_NAME,'address').text

  print("extracted dealers address")

    # address = driver.find_elements(By.XPATH, "//span[(text()='Carr #2 Km 82 Hm 2, Arecibo, PR 00614(18 mi)')]")

  logger.info("Complete dealers details")

  

  return {'name':dealer_name,'url': dealer_url, 'address': address}


if __name__ == "__main__":

    start_time = time.time()

    # url = "https://www.cargurus.com/Cars/dl.action?entityId=&address=castaner+PR+631&latitude=18.1856&longitude=-66.8333&distance=100"

    # print(parse_dealer.dealers)


    #  print("Creating driver")
    #  driver = get_driver()

    # print("multi process start")


    # print("Fetching dealer")
    # dealers = parse_dealer(url)
    # print("finished fetching dealer")
    url = generate_urls()
    
    
  
    p = Pool(5)
    result = p.map(parse_dealer, url)
    p.close()
    p.join()
    print("multi process over")
  
    # x = parse_dealer(url)
  
    # print(f'Found {len(x.dealers)} dealer')
    # print("finished length dealer")
        
    # print("Parsing dealers")
    dealer_data = [parse_dealer(dealer) for dealer in result]
    # print(dealer_data)
    # print("finished dealer details")

  

  
    print("Creating CSV of all dealer details")
    print('Save the data in CSV')
    dealers_df = pd.DataFrame(dealer_data)
    print(dealers_df)
    dealers_df.to_csv('dealer.csv', index=None)


  


    print('\n\t Total time taken:', time.time() - start_time)

    # ThreadPool(5).map(dealers,dealer_data)

    # count = 5
    # for i in range(count):
    #   driverThread = threading.Thread(target=parse_dealer)

    # print("thread start")

    # with Pool(cpu_count()) as p:
    #   p.map(parse_dealer,url)

    # print("thread over")





