import Log
import qrcode
import base64
import platform
import tkinter as tk
from json import load
from io import BytesIO
from time import sleep
from pathlib import Path
from PIL import Image, ImageTk
from os import getcwd, environ
from pyzbar.pyzbar import decode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class Config():

    def __init__(self, Driver):

        try:
            self.PathUser = Path(sys._MEIPASS +  f'/Data/Config/Lang/{environ.get("Language")}/Config.json')
        except Exception:
            self.PathUser = Path(getcwd() +  f'/Data/Config/Lang/{environ.get("Language")}/Config.json')

        self.QRCode = qrcode.QRCode()
        self.Log = Log.Generate()
        self.WebDriver = Driver
        self.Validate = None
        self.UserFileConfig = None

        with open(self.PathConfig, 'r') as UserFileConfig:
            self.AllConfig = load(UserFileConfig)
            self.Welcome = self.AllConfig['welcome']

            UserFileConfig.close()

        self.count = 0
        self.Display = None
        self.CanvasQR = None
        self.OS = platform.system()

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

            User = WebDriverWait(self.WebDriver, 30).until(ec.presence_of_element_located(
                (By.XPATH, f'//span[@title = "{environ.get("ChatName")}"]')))
            User.click()

            return True

        except Exception as error:
            self.Log.Write(f"Config.py | GenericErr - Load Chat # ChatName: {environ.get('ChatName')} Not Found - Change for a valid chat name in the .env file.")
            self.Error = "Error: To initialize bot"
            return False

    def GetWelcome(self):
        return self.Welcome

    def __SessionActive(self):

        try:
            # Validating if the user is logged in whatsapp if shows the QR code it will be necessary to scan for login
            self.Validate = WebDriverWait(self.WebDriver, 15).until(ec.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/canvas')))

            # If you get QR, it returns false since it indicates that you are not logged in.
            if self.Validate:
                return False

        # If you get the error, it means that you are logged in and the function returns true.
        except TimeoutException:
            return True

    def __CreateSession(self):
        try:
            if self.OS == 'Windows' or self.OS == 'Linux':
                self.SetConfigTK()
                self.__UpdateQR()
                self.Display.mainloop()
            else:
                self.TerminalLogin()

            return True

        except ValueError as error:
            self.Log.Write("Config.py | ValueError # " + str(error))
            self.Error = error
            return False
        except Exception as error:
            self.Log.Write("Config.py | GenericErr - Create session # " + str(error))
            return False

    def SetConfigTK(self):
        self.Display = tk.Tk()
        self.Display.title("Andromeda - Authentication")
        self.Display.geometry("400x400")
        self.Display.resizable(False, False)
        tk.Label(self.Display, text="Please", font=("Arial", 15)).pack()
        tk.Label(self.Display, text="Scan QR Code", font=("Arial", 15)).pack()

        self.CanvasQR = tk.Canvas(self.Display, width=300, height=300)
        self.CanvasQR.pack()

    def __UpdateQR(self):
        try:

            self.count += 1

            # Get image QR code
            QRCode64 = base64.b64decode(self.Validate.screenshot_as_base64)
            # Convert image to PIL
            IMG = Image.open(BytesIO(QRCode64))
            # Resize image
            IMG = IMG.resize((300, 300), Image.ANTIALIAS)

            self.IMG = ImageTk.PhotoImage(IMG)
            self.CanvasQR.create_image(0, 0, anchor=tk.NW, image=self.IMG)

            if self.count >= 3:
                self.DestroyTK()
                self.Error = "Error: could not login, limit of attempts exceeded"
                return False

            self.update_id = self.Display.after(10000, self.__UpdateQR)

        except StaleElementReferenceException:
            self.Display.after_cancel(self.update_id)
            self.DestroyTK()
        except Exception as error:
            self.Log.Write("Config.py | GenericErr - Update QR # " + str(error))

    def DestroyTK(self):
        self.Display.quit()
        self.Display.destroy()

    def TerminalLogin(self):

        try:
            while True:

                self.count += 1

                if self.count <= 3:
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

                self.QRCode.clear()
                sleep(10)
        except Exception as error:
            self.Log.Write("Config.py | GenericErr - Terminal Login # " + str(error))
            return False

    def GetError(self):
        return self.Error
