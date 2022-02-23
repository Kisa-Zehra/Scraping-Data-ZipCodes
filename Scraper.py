from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

zip_codes = pd.read_csv("zipcode.csv")
# print(zip_codes)

# for row in zip_codes[['zip']].iterrows():
#     res = str(row[1].values)[1:-1]
#     url = f'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip={res}&distance=100'
#     print(url)

#   https://www.cargurus.com/Cars/dl.action?entityId=&address=Los+Angeles%2C+CA+90001&latitude=33.96979&longitude=-118.24682&distance=100

# https://www.cargurus.com/Cars/dl.action?entityId=&address=LosAngeles+CA+90001&latitude=33.96979&longitude=-118.24682&distance=100

for ind,row in zip_codes.iterrows():
  url = f"https://www.cargurus.com/Cars/dl.action?entityId=&address={row['city_slug']}+{row['state_id']}+{row['zip']}&latitude={row['lat']}&longitude={row['log']}&distance=100"
  #print(url)

url = "https://www.cargurus.com/Cars/dl.action?entityId=&address=castaner+PR+631&latitude=18.1856&longitude=-66.8333&distance=100"

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  
  driver = webdriver.Chrome(options = chrome_options)

  driver.get(url)
  return driver

def get_dealer(driver):
  
  DEALER_DIV_CLASS = 'blade'

  driver.get(url)
  
  dealer = driver.find_elements(By.CLASS_NAME,DEALER_DIV_CLASS)

  return dealer


def parse_dealer(dealer):
  name_tag = dealer.find_element(By.CLASS_NAME, 'details')
  dealer_name = name_tag.text
  
  url_tag = dealer.find_element(By.TAG_NAME,'a')
  url = url_tag.get_attribute('href')


  return{
    'dealer name': dealer_name,
    'url': url
  }


if __name__=="__main__":
  print("Creating driver")
  driver = get_driver()

  print("Fetching dealer")
  dealers = get_dealer(driver)

  print(f'Found {len(dealers)} dealer')

  print('Parsing dealers')

  dealer_data =[parse_dealer(dealer) for dealer in dealers]

  print(dealer_data)


  print('Save the data in CSV')
  dealers_df = pd.DataFrame(dealer_data)
  print(dealers_df)
  dealers_df.to_csv('dealer.csv', index=None)