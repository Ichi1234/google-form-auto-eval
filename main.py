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
        maximum_check = random.randint(1, len(check_box))
        select_box = []
        for _ in range(maximum_check):
            select = random.choice(check_box)
            while select in select_box or select.get_attribute("data-answer-value") in ['', '__other_option__']:
                print(select.get_attribute("data-answer-value"))
                select = random.choice(check_box)
            select.click()


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
            SelectBox().run(key)

        elif val[0] == 'check':
            CheckBox().run(key)

        elif val[0] == 'text':
            TextBox().run(key)
        else:
            random.choice(val).click()


def loop_current_page():
    """Loop for each page."""
    global questions
    for question in questions:
        try:
            q_text = question.find_element(By.CSS_SELECTOR, '[class="M7eMe"]').text

            questions_dict[q_text] = question

        except NoSuchElementException:
            q_text = None

        try:
            select_box = question.find_element(By.CSS_SELECTOR, '[role="listbox"]')
        except NoSuchElementException:
            select_box = None

        try:
            check_box = question.find_element(By.CSS_SELECTOR, '[role="checkbox"]')

        except NoSuchElementException:
            check_box = None

        try:
            text_box = question.find_element(By.CSS_SELECTOR, '[type="text"]')

        except NoSuchElementException:
            text_box = None

        if select_box:
            btn = ['select']

        elif check_box:
            btn = ['check']

        elif text_box:
            btn = ['text']

        else:
            btn = question.find_elements(By.CSS_SELECTOR, '[aria-checked]')

        if q_text is not None:
            q_text_choice[q_text] = []
            add_data_to_question(q_text, btn)


url = "https://forms.gle/3r2Lxe6vTqKLdQfJ6"


# Keep chrome open after program finishes
chrom_options = webdriver.ChromeOptions()
chrom_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrom_options)
driver.get(url)

wait = WebDriverWait(driver, 15)

for _ in range(3):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="M7eMe"]')))

    questions = driver.find_elements(By.CSS_SELECTOR, '[role="listitem"]')

    questions_dict = {}

    q_text_choice = {}

    loop_current_page()
    random_and_select()

    next_btn = driver.find_element(By.CSS_SELECTOR, '[jsname="OCpkoe"]')

    if _ != 2:
        next_btn.click()

    time.sleep(0.14)

