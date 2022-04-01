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
from json import load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Interface:

    def __init__(self, WebDriver):

        with open('Data/Config/Config.json', 'r') as f:
            config = load(f)
            self.Name_Bot = config['main']['Default']['WhatsappName']

            f.close()

        self.Log = Log.Generate()

        self.WebDriver = WebDriver

        self.Chat_List_HTML_Class = "zoWT4"


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