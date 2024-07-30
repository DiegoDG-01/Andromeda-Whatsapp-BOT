from dotenv import load_dotenv
load_dotenv()

import Log
from os import environ
from pathlib import Path
from selenium.webdriver.common.by import By


class Whatsapp_Utils:
    def __init__(self, driver):
        self.Log = Log.Generate()
        self.WebDriver = driver
        self.xpaths = {
            "ClassMessageBox": '//*[@id="main"]/div[3]/div/div[2]/div[3]'
        }

    def __validate_class_name(self, class_name: str) -> bool:
        try:
            if self.WebDriver.find_element_by_class_name(class_name):
                return True
        except Exception as e:
            self.Log.Write(f"Whatsapp_Utils.py | Error trying to validate the class name: {e}")
            return False

    def __find_class_name_by_xpath(self, xpath: str) -> str:
        return self.WebDriver.find_element(By.XPATH, xpath).get_attribute('class')

    def __set_new_class_name(self, key_name: str, xpath: str,) -> bool:
        try:
            class_name = self.__find_class_name_by_xpath(xpath).split(" ")[0]

            if class_name:
                environ[key_name] = class_name
                self.__rewrite_class_name(class_name_key=key_name, new_class_name_value=class_name)
                return True
            else:
                return False
        except Exception as e:
            self.Log.Write(f"Wahtsapp_Utils.py | Error trying to set the new class name: {e}")
            return False

    def __rewrite_class_name(self, class_name_key: str, new_class_name_value: str) -> bool:
        try:
            with open(Path(__file__).parent / '.env', 'r') as file:
                lines = file.readlines()

            with open(Path(__file__).parent / '.env', 'w+') as file:
                for line in lines:
                    if line.startswith(class_name_key):
                        line = f"{class_name_key}='{new_class_name_value}'\n"
                    file.write(line)
            return True
        except Exception as e:
            self.Log.Write(f"Wahtsapp_Utils.py | Error trying to rewrite the xpath: {e}")
            return False

    def check_messagebox(self) -> bool:
        try:
            value = 'ClassMessageBox'
            messageBox_xpath = environ.get(value)

            if self.__validate_class_name(messageBox_xpath):
                return True
            else:
                if not self.__set_new_class_name(key_name=value, xpath=self.xpaths[value]):
                    return False

                return True
        except Exception as e:
            self.Log.Write(f"Wahtsapp_Utils.py | Check_messagebox | Error trying to check the message box: {e}")
            return False
