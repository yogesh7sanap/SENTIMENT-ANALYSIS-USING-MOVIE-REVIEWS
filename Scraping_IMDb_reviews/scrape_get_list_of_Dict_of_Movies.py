import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

## to replace all special symbols
import re

##############################################################################

##1. Get Driver
driver = webdriver.Chrome()

##2. Get the required URL
# ******CHANGE URLS FROM HERE
URL = "https://www.imdb.com/chart/bottom/"

driver.get(URL)

time.sleep(6)
# Wait for the page to load fully
WebDriverWait(driver, 10).until(
    lambda driver: driver.execute_script("return document.readyState") == "complete"
)
time.sleep(6)


wait = WebDriverWait(driver, 10)

# XPath
# **** //ul[@class = "ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 iyTDQy compact-list-view ipc-metadata-list--base"] ****
# list_of_movie_ul_tag =  wait.until(ec.presence_of_element_located(
#             (By.XPATH, '//ul[@class = "ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 iyTDQy compact-list-view ipc-metadata-list--base"]')))

# print(type(list_of_movie_ul_tag));

#-------------------------------------------------------------------------

# list_of_movie_li_tag =  wait.until(ec.presence_of_element_located(
#             (By.XPATH, '//li[@class="ipc-metadata-list-summary-item sc-4929eaf6-0 DLYcv cli-parent"]')))

# print(type(list_of_movie_li_tag));

#--------------------------------------------------------------------------

# list_of_movie_a_tag =  wait.until(ec.presence_of_element_located(
#             (By.CLASS_NAME, '//li[@class="ipc-metadata-list-summary-item sc-4929eaf6-0 DLYcv cli-parent"]//a[@class="ipc-title-link-wrapper"]')))

#--------------------------------------------------------------------------

# list_of_movie_a_tag => contains all the URL of MOVIES (Bottom IMDB - 100)
list_of_movie_a_tag = driver.find_elements(By.XPATH,'//li[@class="ipc-metadata-list-summary-item sc-4929eaf6-0 DLYcv cli-parent"]//a[@class="ipc-title-link-wrapper"]')

print(type(list_of_movie_a_tag))

i=1
#=========================================GETTING LIST OF MOVIES LINK FOR TRAVERSAL=======================
# for storing number and URL -> number will be used for filename
list_of_dictionary_of_movies=[]
for movie_link in list_of_movie_a_tag:
  print(movie_link.text)

  complete_movie_name_with_number = movie_link.text;
  number= complete_movie_name_with_number.split(".")
  number = number[0]
  print(number)

  # Getting Individual MOVIE URL and passing it to driver()
  MOVIE_MAIN_PAGE_URL=movie_link.get_attribute('href');
  print("movie review URL : ",MOVIE_MAIN_PAGE_URL)

  list_of_dictionary_of_movies.append({
      "number":number,
      "URL":MOVIE_MAIN_PAGE_URL
  })



for mv in range(0, 2,1):
  #=============================MAIN MOVIE REVIEW SCRAPING===================================
  # ----------------------------
  l1 = list_of_dictionary_of_movies[mv]['URL'].split('/')

  movie_id = l1[4]
  print("Movie ID", l1[4])


  driver.get(list_of_dictionary_of_movies[mv]['URL'])

  time.sleep(6)
  # Wait for the page to load fully
  WebDriverWait(driver, 10).until(
      lambda driver: driver.execute_script("return document.readyState") == "complete"
  )
  time.sleep(6)


  wait = WebDriverWait(driver, 10)

  #GETTING NUMBER FROM DICT for filename

  number=list_of_dictionary_of_movies[mv]['number']

  #Getting Movie Name for JSON File
  movie_nm = wait.until(ec.presence_of_element_located(
              (By.XPATH, './/span[@class="hero__primary-text"]')))
  print(movie_nm.text);

  file_movie_name=movie_nm.text
  file_movie_name=file_movie_name.strip()
  ### Replace all special symbols with '_'
  file_movie_name = re.sub(r'[^a-zA-Z0-9\s]', '_', file_movie_name)
  file_movie_name=file_movie_name.replace(" ","_")
  # print(f"hey/{number}.{file_movie_name}")
  file_name=f"data{number}.{file_movie_name}"
  print(file_name)

  #Getting Movie Rating
  # movie_rt_get1 = driver.find_element(By.XPATH, '//div[@class="sc-9a2a0028-3 bwWOiy"]')
  # movie_rt = movie_rt_get1.find_element(By.XPATH, '//div[@data-testid="hero-rating-bar__aggregate-rating__score"]')
  # movie_rt = movie_rt_get1.find_element(By.XPATH, ' ')

  movie_rt=""
  movie_rt = wait.until(ec.presence_of_element_located(
              (By.XPATH, '(//span[@class="sc-d541859f-1 imUuxf"])[1]')))
  
  if movie_rt.text=="":
    movie_rt = wait.until(ec.presence_of_element_located(
              (By.XPATH, '(//span[@class="sc-d541859f-1 imUuxf"])[2]')))

  movie_rating=movie_rt.text
  print(movie_rating);


