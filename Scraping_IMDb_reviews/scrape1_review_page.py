import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

##1. Get Driver
driver = webdriver.Chrome()

##2. Get the required URL
# ******CHANGE URLS FROM HERE
URL = "https://www.imdb.com/title/tt0065832/reviews/?ref_=tt_urv_sm"

movie_rating="3.3"

file_movie_name="1.Hercules in New York"

# ----------------------------
l1 = URL.split('/')

movie_id = l1[4]
print("Movie ID", l1[4])


driver.get(URL)

time.sleep(6)
# Wait for the page to load fully
WebDriverWait(driver, 10).until(
    lambda driver: driver.execute_script("return document.readyState") == "complete"
)
time.sleep(6)

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
            (By.XPATH, '//span[@class="ipc-see-more__text" and text()="All"]/ancestor::button')))
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
            (By.XPATH, '//span[@class="ipc-see-more__text" and contains(text(),"more")]/ancestor::button')))
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

    review_articles = driver.find_elements(By.XPATH, '//article[@class="sc-f53ace6f-1 cHwTOl user-review-item"]')
    # wait = WebDriverWait(driver, 10)
    # review_articles = wait.until(ec.presence_of_all_elements_located((By.XPATH, '//article[@class="sc-2b6c2ed6-1 gHSlW user-review-item"]')))

    print(type(review_articles))
    i=0
    for article in review_articles:
        # i+=1
        # if i==5:
        #    break
        # print(type(article.text))

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
    with open(f"JSON_FILES/Test_Complete1/data{file_movie_name}.json", "w") as file:
        json.dump(data, file, indent=4)

    print(f"Length of list is : {len(data)}")
except Exception as e:
    print(f"An error occurred: {e}")

driver.close()































