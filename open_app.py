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

class OpenApplication:
    def __init__(self, url):
      self.url=url

    def open_app(self):
        '''To open particular system URL'''
        global driver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url)
