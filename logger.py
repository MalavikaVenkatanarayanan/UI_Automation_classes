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