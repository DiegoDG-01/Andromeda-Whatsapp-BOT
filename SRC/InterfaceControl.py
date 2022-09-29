###################################
##    ______________________     ##
##    ___    |__  __ \__    |    ##
##    __  /| |_  / / /_  /| |    ##
##    _  ___ |  /_/ /_  ___ |    ##
##    /_/  |_/_____/ /_/  |_|    ##
##                               ##
##       Interface Control       ##
##                               ##
###################################

import Log
import Tabs
from os import getcwd
from json import load
from pathlib import Path
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Libs.Selenium_Screenshot.Screenshot_Clipping as Screenshot_Clipping


class Interface:

    def __init__(self, WebDriver):

        Main_Path = getcwd()
        Path_Config = Path(Main_Path + "/Data/Config/Config.json")


        with open(Path_Config, 'r') as f:
            config = load(f)
            self.Name_Bot = config['main']['Default']['WhatsappName']

            f.close()

        self.Log = Log.Generate()

        self.WebDriver = WebDriver

        self.Chat_List_HTML_Class = "zoWT4"

        self.Path_Screenshot = str(Path(Main_Path + "/Data/WhatsApp/Screenshot/"))

        self.Tabs = Tabs.Tabs(self.WebDriver)

        self.Screenshot = Screenshot_Clipping.Screenshot()

    # Only use to managment the interface for customs modules and not for the main module
    def get_WebDriver(self):
        return self.WebDriver

    def return_to_bot(self):

        User = WebDriverWait(self.WebDriver, 60).until(EC.presence_of_element_located((By.XPATH, f'//span[@title = "{self.Name_Bot}"]')))
        User.click()
        return True

    def change_view(self, Tag):

        try:

            XPath = "//*[@aria-label='Chat list']/div"

            Chat_List = self.WebDriver.find_elements_by_xpath(XPath)

            for Chat in Chat_List:

                user = Chat.find_element(By.CLASS_NAME, "zoWT4").text

                if user == Tag:
                    Chat.click()
                    return True

            self.Log.Write("InterfaceControl.py | Info # Not found user: " + Tag)
            return False

        except Exception as e:
            self.Log.Write("InterfaceControl.py | error # " + str(e))

    def minimize(self):
        self.WebDriver.minimize()

    def maximize(self):
        self.WebDriver.maximize()

    def take_screenshot(self, Name=None):

        try:
            if Name is None:
                alphabet = [letter for letter in range(65, 91)]
                Name = [chr(i) for i in alphabet if randint(0, 1) == 1]

                Name = "".join(Name)
                Name = Name + '.png'

            return self.Screenshot.full_Screenshot(self.WebDriver, save_path=self.Path_Screenshot, image_name=Name,
                                                   multi_images=True)
        except Exception as e:
            self.Log.Write("InterfaceControl.py | Screenshot Error # " + str(e))
            return False

    # This open the menu of whatsapp to send media files under the chat
    def open_menu(self):
        menu_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
        try:
            WebDriverWait(self.WebDriver, 5).until(EC.element_to_be_clickable((By.XPATH, menu_xpath))).click()
            return True
        except Exception as e:
            self.Log.Write("InterfaceControl.py | Error - Open menu # " + str(e))
            return False

    def send_mediafile_button(self):
        button_xpath = '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div'
        try:
            WebDriverWait(self.WebDriver, 5).until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()
            return True
        except Exception as e:
            self.Log.Write("InterfaceControl.py | Error - Send mediafile_button # " + str(e))
            return False

    def send_mediafile(self, file):

        # comprobate if the file exist
        if Path(file).is_file():
            if Path(file).stat().st_size > 2000000:
                return self.send_document(route=file)
            else:
                return self.send_image(route=file)
        else:
            return False, ['File not found']

    # This send image files to the chat in whatsapp
    def send_image(self, image_name=None, route=None):

        if route is None and image_name is None:
            return False

        input_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'

        if route is None:
            image = getcwd() + "/Data/WhatsApp/Screenshot/" + image_name
        else:
            image = route

        if self.open_menu():
            try:
                self.WebDriver.find_element_by_xpath(input_xpath).send_keys(image)
                self.send_mediafile_button()
                return True, ['Image sent']
            except Exception as e:
                self.Log.Write("InterfaceControl.py | Error Send Image # " + str(e))
                return False, ['Error sending image']
        else:
            return False

    # In development
    def send_document(self, name=None, route=None):

        if route is None and name is None:
            return False

        input_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[4]/button/input'

        if route is None:
            image = getcwd() + "/Data/WhatsApp/Screenshot/" + name
        else:
            image = route

        if self.open_menu():
            try:
                self.WebDriver.find_element_by_xpath(input_xpath).send_keys(image)
                self.send_mediafile_button()
                return True, ['Document sent']
            except Exception as e:
                self.Log.Write("InterfaceControl.py | Error - Open menu # " + str(e))
                return False, ['Error sending document']

    # To create new windows is necessary pass name to open
    def create_new_window(self, URL=None):
        if URL is not None:
            return self.Tabs.open(URL)
        else:
            return False

    def close_tabs(self, ID=None):
        try:
            return self.Tabs.close_tab(ID=ID)
        except Exception as e:
            self.Log.Write("InterfaceControl.py | Error - Close tabs # " + str(e))
            return False

    def move_next_tab(self):
        return self.Tabs.move_tab(self.Tabs.active_tab() + 1)

    def move_previous_tab(self):
        return self.Tabs.move_tab(self.Tabs.active_tab() - 1)

    def move_specific_tab(self, position):
        return self.Tabs.move_tab(position)

    def return_to_main_tab(self):
        # The function if not pass the number of tab use the main tab
        return self.Tabs.move_tab()
