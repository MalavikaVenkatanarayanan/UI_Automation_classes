import pandas as pd
import logging  # Added by Mrityunjay on 19th July
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime  # Added by Kajal on 27th Aug
from PIL import Image, ImageDraw, ImageFont
import os
import re
parent_dir = os.getcwd()  # Get current working directory
now = datetime.now()  # Get current date and time
current_time = now.strftime("%d%m%Y_%H%M%S") # Convert current date and time to string


class TestExecution:
    def __init__(self,xpath,current_scenario ):
        self.current_scenario=current_scenario
        self.xpath=xpath

    def construct_xpath(self):
        '''Create final xpath to be passed'''
        x_split = self.xpath.split('("')
        x_split2 = x_split[1].split('"))')
        final_xpath = x_split2[0]
        return final_xpath

    logging.info(f'Scenarios under execution : {scenario_file_path()}')

    get_text = ''
    scenario_to_run = ''

    def run_script(self):
        '''Function definition to execute script of current scenario'''
        global get_text
        global scenario_to_run
        scenario_to_run = self.current_scenario
        logging.info(f"Current scenario executing::: {scenario_to_run}")
        data_path = ('./data/' + scenario_to_run + '.csv')
        log_path = (scenario_to_run + '_' + current_time + '.log')
        logging.info(f"data_path::: {data_path}")
        logging.info(f"log_path::: {log_path}")
        df = pd.read_csv(data_path)
        log_file = log_path
        logging.info(f"log file::: {log_file}")
        enable_log(log_file)
        # Iterate the csv file for Step by Step execution of Events
        for ind in df.index:
            logging.info(f"*** Executing step {ind + 1} ***")
            logging.info(f"Step Executed : {df['Step'][ind]}")
            # Event used to click on elements
            if df['Event'][ind] == "click":
                final_xpath = construct_xpath(df['XPATH'][ind])
                identifier = '"' + final_xpath + '"'
                logging.info(f"identifier:::: {identifier}")
                try:
                    # Wait until element or xpath is present on webpage
                    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, final_xpath)))
                    element.click()
                except:
                    # Providing time delay until xpath is available on page
                    print(f'Click Exception Occured while executing step {ind + 1}')
                    time.sleep(10)
                    WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath(final_xpath)).click()
                takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to send input to elements
            elif df['Event'][ind] == "send_key":
                if get_text != "":
                    if df['Step'][ind] == "Enter Service Order ID":
                        user_input = get_text  # SO ID fetched from previous scenario execution
                        final_xpath = construct_xpath(df['XPATH'][ind])
                        logging.info(f"user input:: {user_input}")
                        identifier = '"' + final_xpath + '"'
                        logging.info(f"identifier:::: {identifier}")
                        try:
                            # Wait until element or xpath is present on webpage
                            element = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((By.XPATH, final_xpath)))
                            element.send_keys(user_input)
                        except:
                            # Providing time delay until xpath is available on page
                            time.sleep(7)
                            WebDriverWait(driver, 30).until(
                                lambda driver: driver.find_element_by_xpath(final_xpath)).send_keys(user_input)
                        takeScreenshot(ind)  # Function call for taking screenshots
                    else:
                        final_xpath = construct_xpath(df['XPATH'][ind])
                        user_input = df['Data'][ind]
                        logging.info(f"user input:: {user_input}")
                        identifier = '"' + final_xpath + '"'
                        logging.info(f"identifier:::: {identifier}")
                        try:
                            # Wait until element or xpath is present on webpage
                            element = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((By.XPATH, final_xpath)))
                            element.send_keys(user_input)
                        except:
                            # Providing time delay until xpath is available on page
                            time.sleep(7)
                            WebDriverWait(driver, 30).until(
                                lambda driver: driver.find_element_by_xpath(final_xpath)).send_keys(user_input)
                        takeScreenshot(ind)  # Function call for taking screenshots
                else:
                    final_xpath = construct_xpath(df['XPATH'][ind])
                    user_input = df['Data'][ind]
                    logging.info(f"user input:: {user_input}")
                    identifier = '"' + final_xpath + '"'
                    logging.info(f"identifier:::: {identifier}")
                    try:
                        # Wait until element or xpath is present on webpage
                        element = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, final_xpath)))
                        element.send_keys(user_input)
                    except:
                        # Providing time delay until xpath is available on page
                        time.sleep(10)
                        WebDriverWait(driver, 30).until(
                            lambda driver: driver.find_element_by_xpath(final_xpath)).send_keys(user_input)
                    takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to press Keyboard's key 'ENTER'
            elif df['Event'][ind] == "keypress":
                logging.info(f"inside key press:---")
                #            time.sleep(5)
                chains = ActionChains(driver)
                chains.send_keys(Keys.ENTER)
                chains.perform()
                #            time.sleep(5)
                takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to Scroll Down the page
            elif df['Event'][ind] == "scroll_down":
                final_xpath = construct_xpath(df['XPATH'][ind])
                logging.info(f"execute scroll function:---")
                try:
                    # Wait until element or xpath is present on webpage
                    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, final_xpath)))
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click_and_hold().perform()
                    time.sleep(10)
                except:
                    # Providing time delay until xpath is available on page
                    time.sleep(10)
                    element = driver.find_element_by_xpath(final_xpath)
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click_and_hold().perform()
                    time.sleep(10)
            # Event used to search the element
            elif df['Event'][ind] == "search":
                final_xpath = construct_xpath(df['XPATH'][ind])
                logging.info(f"X-path:::: {final_xpath}")
                try:
                    # Wait until element or xpath is present on webpage
                    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, final_xpath)))
                    element.click()
                except:
                    # Providing time delay until xpath is available on page
                    time.sleep(10)
                    WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath(final_xpath)).click()
                takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to take some extra screenshots
            elif df['Event'][ind] == "screenshot":
                time.sleep(10)
                takeScreenshot(ind)  # Function call for taking screenshots
            # Event used for refershing the page based on user input
            elif df['Event'][ind] == "refresh":
                user_input = df['Data'][ind]
                time.sleep(int(user_input))
                driver.refresh()
                takeScreenshot(ind)  # Function call for taking screenshots
            # Event used for uploading the files
            elif df['Event'][ind] == "upload":
                final_xpath = construct_xpath(df['XPATH'][ind])
                user_input = df['Data'][ind]
                file_path = os.path.join(parent_dir, 'data_upload', user_input)
                logging.info(f"user input:: {file_path}")
                try:
                    # Wait until element or xpath is present on webpage
                    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, final_xpath)))
                    element.send_keys(file_path)
                except:
                    # Providing time delay until xpath is available on page
                    time.sleep(5)
                    WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath(final_xpath)).send_keys(
                        file_path)
                takeScreenshot(ind)  # Function call for taking screenshots
                time.sleep(5)  # Extra time delay after uploading file
            # Event used to Right click on specified path
            elif df['Event'][ind] == "right_click":
                final_xpath = construct_xpath(df['XPATH'][ind])
                logging.info(f"execute Right click:---")
                try:
                    # Wait until element or xpath is present on webpage
                    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, final_xpath)))
                    actions = ActionChains(driver)
                    actions.context_click(element).perform()
                except:
                    # Providing time delay until xpath is available on page
                    time.sleep(5)
                    element = driver.find_element_by_xpath(final_xpath)
                    actions = ActionChains(driver)
                    actions.context_click(element).perform()
                takeScreenshot(ind)  # Function call for taking screenshots
            elif df['Event'][ind] == "pixel_position":
                logging.info(f"execute pixel position event:---")
                try:
                    # Wait until element or xpath is present on webpage
                    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    action = ActionChains(driver)
                    action.move_to_element_with_offset(element, 790, 290)
                    action.click()
                    action.perform()
                except:
                    # Providing time delay until xpath is available on page
                    time.sleep(10)
                    actions = ActionChains(driver)
                    element = driver.find_element_by_tag_name('body')
                    action = ActionChains(driver)
                    action.move_to_element_with_offset(element, 790, 290)
                    # action.context_click() # for testing purpose using context_click()
                    action.click()
                    action.perform()
            # Event used to Wait for few seconds according to user input
            elif df['Event'][ind] == "wait":
                user_input = df['Data'][ind]
                time.sleep(int(user_input))
            # Event used to click on date from the datepicker
            elif df['Event'][ind] == "datepick":
                final_xpath = construct_xpath(df['XPATH'][ind])
                identifier = '"' + final_xpath + '"'
                logging.info(f"identifier:::: {identifier}")
                try:
                    # Wait until element or xpath is present on webpage
                    element = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, final_xpath)))
                    element.click()
                except:
                    # Providing time delay until xpath is available on page
                    time.sleep(5)
                    WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_css_selector(
                        final_xpath)).click()  # ".dropdown-menu:nth-child(6) > .datepicker-days .active" # example css_selector for active date
                takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to get text present on webpage
            elif df['Event'][ind] == "get_text":
                final_xpath = construct_xpath(df['XPATH'][ind])
                identifier = '"' + final_xpath + '"'
                logging.info(f"identifier:::: {identifier}")
                time.sleep(2)
                get_whole_text = WebDriverWait(driver, 30).until(
                    lambda driver: driver.find_element_by_xpath(final_xpath)).text
                logging.info(f"Get text value:::: {get_whole_text}")
                get_SO = re.search("\d{9}", get_whole_text)  # Get first SO ID displayed on dialog box
                get_text = get_SO.group()
                logging.info(f"final Get text value:::: {get_text}")
            elif df['Event'][ind] == "skip":
                pass
            # Event used to check if field is editable
            elif df['Event'][ind] == "editable":
                final_xpath = construct_xpath(df['XPATH'][ind])
                identifier = '"' + final_xpath + '"'
                logging.info(f"identifier:::: {identifier}")
                # Wait until element or xpath is present on webpage
                element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, final_xpath)))
                editable = element.is_enabled()
                if editable:
                    user_input = df['Data'][ind]
                    element.send_keys(user_input)
                else:
                    try:
                        user_input = df['Data'][ind]
                        element.send_keys(user_input)
                    except:
                        print("Not editable")
            elif df['Event'][ind] == "non_editable":
                try:
                    # Wait until element or xpath is present on webpage
                    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, final_xpath)))
                    element.click()
                except:
                    # Providing time delay until xpath is available on page
                    print(f'Click Exception Occured while executing step {ind + 1}')
                    print("Because Non-editable")
                    print("Hence Passing")
                    pass
            else:
                logging.error(f"No record found:---")
            # Function call to make pdf for all screen shots taken during execution
        testResultPngToPdf(result_type='Pass')

    scenariosToBeExecuted = scenario_file_path()

