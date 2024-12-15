import time
import random

from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class FieldTypeStrategy(ABC):
    """Abstract base class for field handling strategies."""

    @abstractmethod
    def run(self, question_text: str):
        pass


class SelectBox(FieldTypeStrategy):
    """Handles selection of options in dropdown fields."""

    def run(self, question_text: str):
        """Select one of the option"""
        question = questions_dict[question_text]
        select_container = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[role="listbox"]')))

        select_container.click()

        # For me in the future if my code is error it because google change class name.
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.OA0qNb.ncFHed.QXL7Te [aria-selected="false"]')))
        select: list[WebElement] = question.find_elements(By.CSS_SELECTOR, '[role=option]')

        select_choice = random.choice(select)
        while select_choice == select[0]:
            select_choice = random.choice(select)
        select_choice.click()
        time.sleep(0.1)


class TextBox(FieldTypeStrategy):
    """Handles input of text into text fields."""

    def run(self, question_text: str):
        """Type word it to the text field."""
        question = questions_dict[question_text]
        text_box = question.find_element(By.CSS_SELECTOR, '[type="text"]')
        text_box.send_keys('-')


class CheckBox(FieldTypeStrategy):
    """Handles selection of multiple options in checkbox fields."""

    def run(self, question_text: str):
        """Random number to select 1 to n_options."""
        question = questions_dict[question_text]
        check_box = question.find_elements(By.CSS_SELECTOR, '[role="checkbox"]')

        check_box = [cb for cb in check_box if cb.get_attribute("data-answer-value") not in ['', '__other_option__']]

        maximum_check = random.randint(1, len(check_box))
        select_box = []
        for _ in range(maximum_check):
            select = random.choice(check_box)
            while select in select_box:
                select = random.choice(check_box)
            select_box.append(select)

            select.click()

            time.sleep(0.1)


class RadioBox(FieldTypeStrategy):
    """Handles selection of one option in radio box fields."""

    def run(self, question_text: str):
        """Random choice and select it."""
        question = questions_dict[question_text]
        radio_box = question.find_elements(By.CSS_SELECTOR, '[aria-checked]')

        choice = random.choice(radio_box)
        while choice.get_attribute("data-value") in ['', '__other_option__']:
            choice = random.choice(radio_box)
        choice.click()


def loop_current_page():
    """Loop for each page."""
    global questions
    field_type = {
        'check': '[role="checkbox"]',
        'dropdown': '[role="listbox"]',
        'radio': '[role="radio"]',
        'text': '[type="text"]',
    }

    field_strategy = {
        'check': CheckBox,
        'dropdown': SelectBox,
        'text': TextBox,
        'radio': RadioBox,
    }
    for question in questions:
        try:
            q_text = question.find_element(By.CSS_SELECTOR, '[class="M7eMe"]').text

            questions_dict[q_text] = question

        except NoSuchElementException:
            q_text = None

        for key, val in field_type.items():
            try:
                question.find_element(By.CSS_SELECTOR, val)
                question_type = key

                if q_text:
                    field_strategy[question_type]().run(q_text)

                break

            except NoSuchElementException:
                pass


loop_range = int(input("How many submit do you want? \n"))

while loop_range < 1:
    print(f"{loop_range}??? WTF do you mean??")
    loop_range = int(input("How many submit do you want? \n"))

is_not_auto = False
if loop_range == 1:
    is_not_auto = input("Since, you input 1.\n"
                             "Do you want to check the answer first"
                             " before submit? (True/False)\n").lower()

    while is_not_auto not in ['true', 'false']:
        print("PLEASE TYPE TRUE OR FALSE")
        is_not_auto = input("Since, you input 1.\n"
                                 "Do you want to check the answer first"
                                 " before submit? (True/False)\n").lower()

if is_not_auto == 'true':
    is_not_auto = True

elif is_not_auto == 'false':
    is_not_auto = False

url = "https://forms.gle/3r2Lxe6vTqKLdQfJ6"


chrom_options = webdriver.ChromeOptions()
chrom_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrom_options)
driver.get(url)

wait = WebDriverWait(driver, 15)


while loop_range:
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="M7eMe"]')))

    questions = driver.find_elements(By.CSS_SELECTOR, '[role="listitem"]')

    questions_dict = {}

    loop_current_page()

    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, '[jsname="OCpkoe"]')
        next_btn.click()

    except NoSuchElementException:
        submit_btn = driver.find_element(By.CSS_SELECTOR, '[jsname="M2UYVd"]')

        if not is_not_auto:
            submit_btn.click()
            driver.get(url)
        else:
            break

        loop_range -= 1


    time.sleep(0.14)

