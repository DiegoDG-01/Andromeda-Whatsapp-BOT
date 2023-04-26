import Log
import time
import qrcode
import base64
from PIL import Image
from os import getcwd
from json import load
from io import BytesIO
from pathlib import Path
from pyzbar.pyzbar import decode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from  selenium.common.exceptions import TimeoutException

class Config():

    def __init__(self, Driver):

        self.QRCode = qrcode.QRCode()
        self.Log = Log.Generate()
        self.WebDriver = Driver
        self.PathUser = Path(getcwd() + '/Data/Config/Config.json')
        self.Validate = None
        self.UserFileConfig = None

        with open(self.PathUser, 'r') as UserFileConfig:
            self.AllConfig = load(UserFileConfig)

            self.UFC = self.AllConfig['main']
            self.Welcome = self.AllConfig['welcome']

            UserFileConfig.close()


    def Initialize(self):

            if self.__SessionActive():
                self.__load_chat()
                return True
            else:
                if self.__CreateSession():
                    self.__load_chat()
                    return True
                else:
                    return False


    def __load_chat(self):
        try:

            User = WebDriverWait(self.WebDriver, 60).until(ec.presence_of_element_located(
                (By.XPATH, '//span[@title = "{}"]'.format(self.UFC['Default']["WhatsappName"]))))
            User.click()

            return True

        except Exception as error:
            self.Log.Write("Config.py | GenericErr - Load Chat # " + str(error))
            self.Error = "Error: To initialize bot"
            return False

    def GetWelcome(self):
        return self.Welcome

    def __SessionActive(self):

        try:
            # Validating if the user is logged in whatsapp if shows the QR code it will be necessary to scan for login
            self.Validate = WebDriverWait(self.WebDriver, 15).until(ec.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/canvas')))

            # If you get QR, it returns false since it indicates that you are not logged in.
            if self.Validate:
                return False

        # If you get the error, it means that you are logged in and the function returns true.
        except TimeoutException:
            return True

    def __CreateSession(self):

        count = 1

        while True:
            try:
                if count <= 3:
                    # Get image QR code
                    QRCode64 = base64.b64decode(self.Validate.screenshot_as_base64)
                    # Convert image to PIL
                    IMG = Image.open(BytesIO(QRCode64))
                    # Decode QR code data
                    DataQR = decode(IMG)[0].data.decode('utf-8')

                    # Load QR code data to convert string to QR code Ascii & print QR code in terminal
                    self.QRCode.add_data(DataQR)

                    # Print in terminal basic instructions
                    print("\033[93m" + "SCAN QR CODE TO LOGIN" + "\033[0m")
                    self.QRCode.print_ascii(invert=True)

                else:
                    self.Error = "Error: could not login, limit of attempts exceeded"
                    return False

                count += 1
                self.QRCode.clear()
                time.sleep(10)

            except ValueError as error:
                self.Log.Write("Config.py | ValueError # " + str(error))
                self.Error = error
                return False
            except Exception as error:
                self.Log.Write("Config.py | GenericErr - Create session # " + str(error))
                return True


    def GenerateUser(self):
        print("Generating new user...")
        pass

    def GetError(self):
        return self.Error