import time
import Log
import base64
from PIL import Image
from io import BytesIO
from os import getcwd
from json import load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from  selenium.common.exceptions import TimeoutException

class Config():

    def __init__(self, Driver):
        self.Log = Log.Generate()
        self.WebDriver = Driver
        self.PathUser = getcwd() + '/Data/Config/Config.json'
        self.Validate = None
        self.UserFileConfig = None

        with open(self.PathUser, 'r') as UserFileConfig:
            self.AllConfig = load(UserFileConfig)

            self.UFC = self.AllConfig['main']
            self.Welcome = self.AllConfig['welcome']

            UserFileConfig.close()


    def Initialize(self):

            if(self.__SessionActive()):
                try:

                    User = WebDriverWait(self.WebDriver, 60).until(ec.presence_of_element_located((By.XPATH, '//span[@title = "{}"]'.format(self.UFC['Default']["WhatsappName"]))))
                    User.click()

                    return True

                except Exception as error:
                    self.Log.Write("Config.py | GenericErr # "+ str(error))
                    self.Error = "Error: To initialize bot"
                    return False
            else:
                self.__CreateSession()

    def GetWelcome(self):
        return self.Welcome

    def __SessionActive(self):

        try:
            # Validating if the user is logged in whatsapp if shows the QR code it will be necessary to scan for login
            self.Validate = WebDriverWait(self.WebDriver, 5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]/div/canvas')))

            # If you get QR, it returns false since it indicates that you are not logged in.
            if self.Validate:
                return False

        # If you get the error, it means that you are logged in and the function returns true.
        except TimeoutException:
            return True

    def __CreateSession(self):

        count = 1

        while(True):

            if (count <= 3):
                QRCode = base64.b64decode(self.Validate.screenshot_as_base64)
                Image.open(BytesIO(QRCode)).show()

                print("Scan the QR code to login.")

            else:
                self.Error = "Error: could not login, limit of attempts exceeded"
                return False

            count += 1
            time.sleep(10)


    def GenerateUser(self):
        print("Generating new user...")
        pass

    def GetError(self):
        return self.Error