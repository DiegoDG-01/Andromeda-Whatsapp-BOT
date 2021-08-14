from os import getcwd
from json import load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Config():
    
    def __init__(self, WebDriver):
        
        PathUser = getcwd() + '/Data/Config/User.json'
        
        with open(PathUser, 'r') as UserFileConfig:
            Data = load(UserFileConfig)
            
            User = WebDriverWait(WebDriver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[@title = "{}"]'.format(Data['main']['WhatsappName']))))
            User.click()
        
    def GenerateUser(self):
        print("Generating new user...")