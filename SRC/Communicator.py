######################################
######################################
##                                  ##
##            /\                    ##
##        _  / |         .'         ##
##       (  /  |  . .-..'  .-.      ##
##        `/.__|_.':   ;  ;   :     ##
##    .:' /    |   `:::'`.`:::'-'   ##
##   (__.'     `-'                  ##
##                                  ##
##              Speaker             ##
##                                  ##
######################################
######################################


import Log
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Communicate:

    def __init__(self, WebDriver):
        self.WebDriver = WebDriver
        self.Log = Log.Generate()

        self.ClassBoxMessage = "_1Gy50"
        self.ClassButton_Send_Xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'

    def WriteMessage(self, msg):

        """[summary]
        """

        try:

            if (type(msg) == str):
                msg = [msg]

            msg_box = WebDriverWait(self.WebDriver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')))
            msg_box.click()

            for i in msg:
                msg_box.send_keys(i + (Keys.SHIFT + Keys.ENTER))
                sleep(0.5)

            return True

        except Exception as e:
            self.Log.Write("communicator.py | error # " + str(e))
            return False

    def SendMessage(self):

        """[summary]
        """

        try:

            # ClassButton_Send = "_4sWnG"

            # button = WebDriverWait(self.WebDriver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, ClassButton_Send)))
            button = WebDriverWait(self.WebDriver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))

            button = self.WebDriver.find_elements_by_xpath(self.ClassButton_Send_Xpath)[0]
            button.click()

            return True

        except Exception as e:
            print("ERROR SendMessage")
            self.Log.Write("communicator.py | error # " + str(e))
            return False

    def ReadResponse(self):


        try:

            "USE THIS METHOD TO READ ONLY LAST MESSAGE IN THE BOT file"
            XPath = "//*[contains(@class, '" + self.ClassBoxMessage + "')]"

            LastMessage = self.WebDriver.find_elements_by_xpath(XPath)[-1:]

            if LastMessage:
                LastMessage = LastMessage.pop().text.split("\n")[0]

                if(LastMessage[0] != "#" and LastMessage[0] != ">"):
                    return LastMessage
                else:
                    return False
            else:
                return False

        except Exception as e:
            self.Log.Write("communicator.py | error # " + str(e))
            return False

    def ReadMediaResponse(self, Class):

        try:

            XPath = "//*[contains(@class, '" + self.ClassBoxMessage + "')]"

            LastMessage = WebDriverWait(self.WebDriver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, Class)))[-1]

            if LastMessage:

                Location_Messages =  self.WebDriver.find_elements_by_xpath(XPath)[-1].location
                Location_Media = LastMessage.location

                if(Location_Messages["y"] < Location_Media["y"]):
                    return True
                else:
                    return False
            else:
                return False

        except Exception as e:
            return False