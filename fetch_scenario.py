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

class FetchScenario:
    def __init__(self, xpath):
        self.xpath=xpath
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