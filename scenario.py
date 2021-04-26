# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:01:23 2020
"""
#Multiple and Multiline inheritance by Malavika
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
#from lxml import html
#import requests
#from selenium.common.exceptions import TimeoutException, NoAlertPresentException
#from selenium.webdriver.common.alert import Alert
#import pdb

#url = 'http://10.144.97.109:9004/cwf/login'  # OC URL
#url='http://10.135.34.37:8111/siteforge/jsp/login.jsp'# SF URL
#url ='http://10.144.97.98:8111/siteforge/jsp/login.jsp' # SF URL2
#url = 'http://10.135.26.21:8079/siteforge/jsp/login.jsp' # SF SIT
#url='http://10.144.96.183:7532/OPI/'# GI GUI URL
parent_dir = os.getcwd()  # Get current working directory
now = datetime.now()  # Get current date and time
current_time = now.strftime("%d%m%Y_%H%M%S") # Convert current date and time to string


class Driver:
    def __init__(self, url):
      self.url=url

    def open_app(self):
        '''To open particular system URL'''
        global driver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url)

class Logger:
    def __init__(self, log_file):
      self.log_file= log_file
    def enable_log(self):
        '''Function definition to set log handler'''
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=os.path.join(parent_dir, 'logs', self.log_file),
                            format='%(asctime)s %(message)s',
                            filemode='w')  # Added for logging information.
        logger = logging.getLogger()  # Creating logger object
        logger.setLevel(logging.DEBUG)  # Setting the threshold of logger to DEBUG

class Screenshots:
    screenshots_list = []  # Storing list of all screenshot pngs captured
    def __init__(self, ind):
      self.ind= ind
    def takeScreenshot(self):
        '''function used to take screenshots for each event'''
        logging.info(f"Screenshots captured!")
        filename = "temp/" + scenario_to_run + "_" + str(self.ind) + ".png"
        driver.get_screenshot_as_file(filename)
        global screenshots_list
        image = Image.open(filename)
        image = image.convert("RGB")
        screenshots_list.append(image)

class Watermark:
    def pass_fail_watermark(result_type, last_image):
        '''Create Pass/Fail Watermark on last_image based on result_type'''
        im = last_image
        width, height = im.size
        draw = ImageDraw.Draw(im)
        text = result_type
        font = ImageFont.truetype('arial.ttf', 36)
        textwidth, textheight = draw.textsize(text, font)
        # calculate the x,y coordinates of the text
        margin = 10
        x = width / 2 - margin
        y = height / 2 - margin
        # Draw watermark in the centre of the page
        if result_type == 'Pass':
            fill = (0, 128, 0)
        else:
            fill = (255, 0, 0)
        draw.text((x, y), text, font=font, fill=fill)
        # draw watermark in the bottom right corner
        # x = width - textwidth - margin
        # y = height - textheight - margin
        # draw.text((x, y), text, font=font)
        im.save("temp/" + scenario_to_run + "_" + "lastImage" + ".png")  # Save watermarked image
        return im


class PngToPdf:
    def __init__(self, result_type):
        self.result_type=result_type
    def testResultPngToPdf(self):
        '''Function call to make pdf for all screen shots taken during execution'''
        logging.info(f"Total Screenshots captured : {len(screenshots_list)}")
        screenshots_list[-1] = super().pass_fail_watermark(self.result_type, screenshots_list[-1])
        pdf_filename = ("TestResults/" + scenario_to_run + "_" + current_time + "_" + self.result_type + ".pdf")
        screenshots_list[0].save(pdf_filename, "PDF", resolution=100.0,
                                 save_all=True, append_images=screenshots_list[1:])
        screenshots_list.clear()


class Path:

    def __init__(self, xpath):
        super().__init__(xpath)
    path_scenario = './data/Scenario.csv'  # Path to fetch Scenario file

    scenario = pd.read_csv(path_scenario)  # Read Scenario.csv file
    global scenario

    def scenario_file_path(self):
        '''Function definition to fetch the scenario with value as "Y" from csv'''
        scenario_to_run_list = []
        for i in scenario.index:
            if scenario['Flag'][i] == 'Y':
                scenario_to_run_list.append(scenario['Scenario'][i])
            else:
                logging.info(f"No scenarios found to be run:---")
        return scenario_to_run_list

    def construct_xpath(self):
        '''Create final xpath to be passed'''
        x_split = self.xpath.split('("')
        x_split2 = x_split[1].split('"))')
        final_xpath = x_split2[0]
        return final_xpath

    logging.info(f'Scenarios under execution : {scenario_file_path()}')

    get_text = ''
    scenario_to_run = ''

class Run_Script(Driver, PngToPdf, Watermark, Screenshots, Logger, Path):    #multiple inheritance
    def __init__(self, current_scenario):
        super().__init__(self)  #Calling the init methods of parent class using super
        self.current_scenario=current_scenario
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
        super().enable_log(log_file)
        # Iterate the csv file for Step by Step execution of Events
        for ind in df.index:
            logging.info(f"*** Executing step {ind + 1} ***")
            logging.info(f"Step Executed : {df['Step'][ind]}")
            # Event used to click on elements
            if df['Event'][ind] == "click":
                final_xpath = super().construct_xpath(df['XPATH'][ind])
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
                super().takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to send input to elements
            elif df['Event'][ind] == "send_key":
                if get_text != "":
                    if df['Step'][ind] == "Enter Service Order ID":
                        user_input = get_text  # SO ID fetched from previous scenario execution
                        final_xpath = super().construct_xpath(df['XPATH'][ind])
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
                        super().takeScreenshot(ind)  # Function call for taking screenshots
                    else:
                        final_xpath = super().construct_xpath(df['XPATH'][ind])
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
                        super().takeScreenshot(ind)  # Function call for taking screenshots
                else:
                    final_xpath = super().construct_xpath(df['XPATH'][ind])
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
                    super().takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to press Keyboard's key 'ENTER'
            elif df['Event'][ind] == "keypress":
                logging.info(f"inside key press:---")
                #            time.sleep(5)
                chains = ActionChains(driver)
                chains.send_keys(Keys.ENTER)
                chains.perform()
                #            time.sleep(5)
                super().takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to Scroll Down the page
            elif df['Event'][ind] == "scroll_down":
                final_xpath = super().construct_xpath(df['XPATH'][ind])
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
                final_xpath = super.construct_xpath(df['XPATH'][ind])
                logging.info(f"X-path:::: {final_xpath}")
                try:
                    # Wait until element or xpath is present on webpage
                    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, final_xpath)))
                    element.click()
                except:
                    # Providing time delay until xpath is available on page
                    time.sleep(10)
                    WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath(final_xpath)).click()
                super.takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to take some extra screenshots
            elif df['Event'][ind] == "screenshot":
               time.sleep(10)
               super.takeScreenshot(ind)  # Function call for taking screenshots
            # Event used for refershing the page based on user input
            elif df['Event'][ind] == "refresh":
                user_input = df['Data'][ind]
                time.sleep(int(user_input))
                driver.refresh()
                super.takeScreenshot(ind)  # Function call for taking screenshots
            # Event used for uploading the files
            elif df['Event'][ind] == "upload":
                final_xpath = super.construct_xpath(df['XPATH'][ind])
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
                super.takeScreenshot(ind)  # Function call for taking screenshots
                time.sleep(5)  # Extra time delay after uploading file
            # Event used to Right click on specified path
            elif df['Event'][ind] == "right_click":
                final_xpath = super.construct_xpath(df['XPATH'][ind])
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
                super.takeScreenshot(ind)  # Function call for taking screenshots
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
                final_xpath = super.construct_xpath(df['XPATH'][ind])
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
                super.takeScreenshot(ind)  # Function call for taking screenshots
            # Event used to get text present on webpage
            elif df['Event'][ind] == "get_text":
                final_xpath = super.construct_xpath(df['XPATH'][ind])
                identifier = '"' + final_xpath + '"'
                logging.info(f"identifier:::: {identifier}")
                time.sleep(2)
                get_whole_text = WebDriverWait(driver, 30).until(
                    lambda driver: driver.find_element_by_xpath(final_xpath)).text
                logging.info(f"Get text value:::: {get_whole_text}")
                get_SO = re.search("\d{9}", get_whole_text)  # Get first SO ID displayed on dialog box
                get_text = get_SO.group()
                logging.info(f"final Get text value:::: {get_text}")
                # logging.info(f"Get text value:::: {get_whole_text}")
                # get_SO = re.findall(r"\b\d{9}\b", get_whole_text)
                # logging.info(f"final Get text value:::: {get_SO[0]}")
                # get_text = get_SO[0]
                # logging.info(f"final Get text value:::: {get_text}")
            elif df['Event'][ind] == "skip":
                pass
            # Event used to check if field is editable
            elif df['Event'][ind] == "editable":
                final_xpath = super.construct_xpath(df['XPATH'][ind])
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
                        user_input = df['Data'][self.ind]
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
                    print(f'Click Exception Occured while executing step {self.ind + 1}')
                    print("Because Non-editable")
                    print("Hence Passing")
                    pass
            else:
                logging.error(f"No record found:---")
        # Function call to make pdf for all screen shots taken during execution
        super.testResultPngToPdf(result_type='Pass')


class Url(Run_Script):
    def __init__(self, url):
        self.url = url
    def UrlLoop(self):
        scenariosToBeExecuted = super.scenario_file_path()
        for i in scenariosToBeExecuted:
            if "OC" in i:
                url = 'http://10.144.97.109:9004/cwf/login'
            elif "GI" in i:
                url = 'http://10.144.96.183:7532/OPI/'
            elif "SF" in i:
                url = 'http://10.135.34.37:8111/siteforge/jsp/login.jsp'
            super.open_app(self.url)
            try:
                super.run_script(i)  # Function call for execution of script
            except:
                logging.exception(f"Time Out Exception:---")
                super.testResultPngToPdf(result_type='Fail')
            driver.close()  # commnet for testing



