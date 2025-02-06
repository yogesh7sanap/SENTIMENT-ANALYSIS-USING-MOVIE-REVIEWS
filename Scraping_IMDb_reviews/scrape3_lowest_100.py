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

#=====================================================================================
#=====================================================================================
i=1
# ----for each loop -> to get all movies data
# for movie_link in list_of_dictionary_of_movies:

## ----To get Data of first 10 Movies
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
              (By.XPATH, '//span[@class="hero__primary-text"]')))
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
  # movie_rt = wait.until(ec.presence_of_element_located(
  #             (By.XPATH, '//div[@class="sc-9a2a0028-3 bwWOiy"]//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[1]')))
  # movie_rt_get1 = driver.find_element(By.XPATH, './/div[@class="sc-9a2a0028-3 bwWOiy"]')
  # movie_rt = movie_rt_get1.find_element(By.XPATH, './/div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[1]')


  movie_rt=""
  movie_rt = wait.until(ec.presence_of_element_located(
              (By.XPATH, '(//span[@class="sc-d541859f-1 imUuxf"])[1]')))
  
  if movie_rt.text=="":
    movie_rt = wait.until(ec.presence_of_element_located(
              (By.XPATH, '(//span[@class="sc-d541859f-1 imUuxf"])[2]')))

  movie_rating=movie_rt.text
  print(movie_rating);

  #==========================================================================================
  # Code to get URL and movie reviews page URL
  #==========================================================================================

  # Locate the element you want to scroll to
  # ****  //div[@data-testid="reviews-header"]//a[@class='ipc-title-link-wrapper']  ****
  movie_review_link_a_tag_button= wait.until(ec.presence_of_element_located(
              (By.XPATH, './/div[@data-testid="reviews-header"]//a[@class="ipc-title-link-wrapper"]')))

  # Scroll to the element using JavaScript
  driver.execute_script("arguments[0].scrollIntoView();", movie_review_link_a_tag_button)

  # print("button text",movie_review_link_a_tag_button.text)

  MOVIE_REVIEW_PAGE_URL=movie_review_link_a_tag_button.get_attribute('href');

  print("movie review URL : ",MOVIE_REVIEW_PAGE_URL)

  time.sleep(6)
  driver.get(MOVIE_REVIEW_PAGE_URL)
  # movie_review_link_a_tag_button.click()
  time.sleep(6)

  # Wait for the page to load fully
  WebDriverWait(driver, 10).until(
      lambda driver: driver.execute_script("return document.readyState") == "complete"
  )
  time.sleep(6)
  #==========================================================================================
    # After going to review page code
  # =========================================================================================
  try:
      wait=''
      button=''
      try:
          # Wait until the button is clickable
          wait = WebDriverWait(driver, 10)
          # button = wait.until(ec.element_to_be_clickable((By.XPATH, '//span[text()="All"]/ancestor::button')))
          # //span[text()="All"]/ancestor::button

          # Locate the element you want to scroll to
          # ****  //span[@class="ipc-see-more__text" and text()="All"]  ****
          button = wait.until(ec.presence_of_element_located(
              (By.XPATH, './/span[@class="ipc-see-more__text" and text()="All"]/ancestor::button')))
          # Scroll to the element using JavaScript
          driver.execute_script("arguments[0].scrollIntoView();", button)

          time.sleep(6)
          button.click()
          time.sleep(6)

      except ElementNotInteractableException:
          wait = WebDriverWait(driver, 10)
          # button = wait.until(ec.element_to_be_clickable((By.XPATH, '//span[text()="All"]/ancestor::button')))
          # //span[text()="All"]/ancestor::button

          # Locate the element you want to scroll to
          # ****  //span[@class="ipc-see-more__text" and text()="All"]  ****
          button = wait.until(ec.presence_of_element_located(
              (By.XPATH, './/span[@class="ipc-see-more__text" and contains(text(),"more")]/ancestor::button')))
          # Scroll to the element using JavaScript
          driver.execute_script("arguments[0].scrollIntoView();", button)

          time.sleep(6)
          button.click()
          time.sleep(6)

  # ---------------------------STORING AND GETTING IMPORTANT DATA
      data = []

      # -------------------------GETTING ALL IMPORTANT DATA
      movie_name = wait.until(ec.element_to_be_clickable((By.TAG_NAME, 'h2')))
      print(movie_name.text)
      #
      movie_name = movie_name.text

      # -----------SCROLLING TO THE END OF PAGE 3 TIMES---------------------
      try:
          # Scroll to the bottom of the page
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          time.sleep(3)  # wait for more reviews to load
      except Exception as e:
          print(f"Scrolling error: {e}")

      time.sleep(5)
      try:
          # Scroll to the bottom of the page
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          time.sleep(3)  # wait for more reviews to load
      except Exception as e:
          print(f"Scrolling error: {e}")

      time.sleep(5)
      try:
          # Scroll to the bottom of the page
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          time.sleep(3)  # wait for more reviews to load
      except Exception as e:
          print(f"Scrolling error: {e}")
      # ----------------------------------------------

      review_articles = driver.find_elements(By.XPATH, './/article[@class="sc-d59f276d-1 euAsTr user-review-item"]')
      # wait = WebDriverWait(driver, 10)
      # review_articles = wait.until(ec.presence_of_all_elements_located((By.XPATH, '//article[@class="sc-2b6c2ed6-1 gHSlW user-review-item"]')))

      print(type(review_articles))
      j=1
      for article in review_articles:
          j+=1
          if j==5:
             break
          print(type(article.text))

          # ****
          # will only // all will be considered hence error was coming
          # review_title = article.find_element(By.XPATH, '//span[contains(@class,"sc-77f6e511-7")]')

          # ---------------------------REVIEW TITLE----------------------
          review_title=''
          try:
              review_title = article.find_element(By.XPATH, './/h3[@class="ipc-title__text"]')
              review_title=review_title.text
          except NoSuchElementException:
              print("Review detailed main content not found. Skipping this article.")
              review_detailed_main = ""
          print(review_title)
          print("----\n")

          #
          # ---------------------------DETAILED REVIEW----------------------
          # -------------------HANDLING NO SUCH ELEMENT BECUASE DETAILED REVIEW NOT PRESENT
          # review_detailed_main = article.find_element(By.XPATH, './/div[@class="ipc-html-content-inner-div"]')
          # review_detailed_main =review_detailed_main.text
          # print(review_detailed_main)

          review_detailed_main=''
          try:
              #review_detailed_main is a serializable object hence we use .text
              review_detailed_main = article.find_element(By.XPATH, './/div[@class="ipc-html-content-inner-div"]')
              review_detailed_main =review_detailed_main.text
          except NoSuchElementException:
              print("Review detailed main content not found. Skipping this article.")
              review_detailed_main = ""

          print("----\n")

          # ---------------------------rating----------------------
          review_rating=''
          try:
              review_rating = article.find_element(By.XPATH, './/span[@class="ipc-rating-star--rating"]')
              review_rating=review_rating.text
          except NoSuchElementException:
              print("Review detailed main content not found. Skipping this article.")
              review_detailed_main = ""
          print(review_rating)
          print("----\n")

          # ---------------------------username----------------------
          review_username = ''
          try:
              review_user_details = article.find_elements(By.XPATH, './/div[@class="sc-f6867cfd-1 iHZNcU"]')
              #
              review_username = ''
              for user_details in review_user_details:
                  user_details_li0 = user_details.find_elements(By.TAG_NAME, 'li')
                  review_username = user_details_li0[0].text
                  break

          except NoSuchElementException:
              print("Review detailed main content not found. Skipping this article.")
              review_detailed_main = ""

          print(review_username)

          data_obj = {
              "movie_id": movie_id,
              "movie_name": movie_name,
              "movie_rating" : movie_rating,
              "review_username": review_username,
              "review_rating" : review_rating,
              "review_title" :review_title,
              "review_detailed_main" : review_detailed_main
          }

          data.append(data_obj)
          # break;


      # --------------------------STORING ALL DATA IN JSON FILE------------------------------------------

      # ---------------1-20
      # with open(f"JSON_FILES/FIRST100/data{file_movie_name}.json", "w") as file:
      #     json.dump(data, file, indent=4)

      # ---------------21-40
      with open(f"JSON_FILES/Test_Complete3/{file_name}.json", "w") as file:
          json.dump(data, file, indent=4)

      print(f"Length of list is : {len(data)}")
      print("movie Link : ",movie_link)
  except Exception as e:
      print(f"An error occurred: {e}")


#=====================================================================================
#=====================================================================================

driver.close()


  

