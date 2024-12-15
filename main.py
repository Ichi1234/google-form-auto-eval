import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def add_data_to_question(question_text: str,  data_list: list):
    """Class for add choice to the question in q_text_choice dict."""
    global q_text_choice
    for data in data_list:
        try:
            if data.get_attribute('data-value') not in ['', '__other_option__']:
                q_text_choice[question_text].append(data)

        except AttributeError:
            q_text_choice[question_text].append(data)


def random_and_select():
    """Class for random choice and select choice for every question."""
    global q_text_choice
    for key, val in q_text_choice.items():
        if val[0] == 'select':
            select_type(key)

        else:
            random.choice(val).click()


def select_type(name):
    """Function for select box only (This fucking box make this project waste of my time)."""
    question = questions_dict[name]
    select_container = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[role="listbox"]')))

    select_container.click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.OA0qNb.ncFHed.QXL7Te [aria-selected="false"]')))
    select: list[WebElement] = question.find_elements(By.CSS_SELECTOR, '[role=option]')

    select_choice = random.choice(select)
    while select_choice == select[0]:
        select_choice = random.choice(select)
    select_choice.click()
    time.sleep(0.1)

url = "https://forms.gle/3r2Lxe6vTqKLdQfJ6"


# Keep chrome open after program finishes
chrom_options = webdriver.ChromeOptions()
chrom_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrom_options)
driver.get(url)

wait = WebDriverWait(driver, 10)

questions = driver.find_elements(By.CSS_SELECTOR, '[role="listitem"]')

questions_dict = {}
radio_btn = driver

q_text_choice = {}
for questions in questions:
   q_text = questions.find_element(By.CSS_SELECTOR, '.M7eMe').text

   questions_dict[q_text] = questions

   try:
       select_box = questions.find_element(By.CSS_SELECTOR, '[role="listbox"]')
   except NoSuchElementException:
       select_box = None

   if select_box:
       btn = ['select']
   else:
       btn = questions.find_elements(By.CSS_SELECTOR, '[aria-checked]')

   # Create ActionChains object
   actions = ActionChains(driver)

   # Perform a click at (x, y) coordinates
   actions.move_by_offset(30, 34).click().perform()

   q_text_choice[q_text] = []
   add_data_to_question(q_text, btn)

random_and_select()

