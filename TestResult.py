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


class TestExecutionResult:
    screenshots_list = []  # Storing list of all screenshot pngs captured

    def __init__(self, ind,result_type,last_image):
        self.ind = ind
        self.last_image=last_image
        self.result_type=result_type

    def takeScreenshot(self):
        '''function used to take screenshots for each event'''
        logging.info(f"Screenshots captured!")
        filename = "temp/" + scenario_to_run + "_" + str(self.ind) + ".png"
        driver.get_screenshot_as_file(filename)
        global screenshots_list
        image = Image.open(filename)
        image = image.convert("RGB")
        screenshots_list.append(image)

    def pass_fail_watermark(self):
        '''Create Pass/Fail Watermark on last_image based on result_type'''
        im =self.last_image
        width, height = im.size
        draw = ImageDraw.Draw(im)
        text = self.result_type
        font = ImageFont.truetype('arial.ttf', 36)
        textwidth, textheight = draw.textsize(text, font)
        # calculate the x,y coordinates of the text
        margin = 10
        x = width / 2 - margin
        y = height / 2 - margin
        # Draw watermark in the centre of the page
        if self.result_type == 'Pass':
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


    def testResultPngToPdf(self):
        '''Function call to make pdf for all screen shots taken during execution'''
        logging.info(f"Total Screenshots captured : {len(screenshots_list)}")
        screenshots_list[-1] = super().pass_fail_watermark(self.result_type, screenshots_list[-1])
        pdf_filename = ("TestResults/" + scenario_to_run + "_" + current_time + "_" + self.result_type + ".pdf")
        screenshots_list[0].save(pdf_filename, "PDF", resolution=100.0,
                                 save_all=True, append_images=screenshots_list[1:])
        screenshots_list.clear()