########################################################
########################################################
##                                                    ##
##                                                    ##
## I8,        8        ,8I  88888888ba   88888888ba   ##
## `8b       d8b       d8'  88      "8b  88      "8b  ##
##  "8,     ,8"8,     ,8"   88      ,8P  88      ,8P  ##
##   Y8     8P Y8     8P    88aaaaaa8P'  88aaaaaa8P'  ##
##   `8b   d8' `8b   d8'    88""""""8b,  88""""""8b,  ##
##    `8a a8'   `8a a8'     88      `8b  88      `8b  ##
##     `8a8'     `8a8'      88      a8P  88      a8P  ##
##      `8'       `8'       88888888P"   88888888P"   ##
##                                                    ##
##                 Whatsapp Browser Bot               ##
##                                                    ##
########################################################
########################################################

import Bot
import Config
from os import getcwd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def InitWebDriver():
    
    URL = 'https://web.whatsapp.com/'
    
    PathSession = getcwd() + '/Data/Session/'
    
    _Chrome_options = Options()
    _Chrome_options.add_argument('--user-data-dir='+PathSession)
    _Chrome_options.add_argument('--disable-extensions')
    _Chrome_options.add_argument('--disable-dev-shm-usage')
    _Chrome_options.add_argument('--no-sandbox')
    
    # Iniciar sin mostrar la ventana del navegador
    # _Chrome_options.add_argument('headless')
     
    try:
        WebDriver = Chrome(options = _Chrome_options)   

        WebDriver.maximize_window()
        WebDriver.get(URL)
        
        return WebDriver
    except:
        WebDriver.quit()
        print('Error')

if(__name__ == '__main__'):
    
    try:
    
        WebDriver = InitWebDriver()
        
        Bot = Bot.Bot()
        Config = Config.Config(WebDriver)
        
        Bot.ReadMessage(WebDriver)
        
        WebDriver.quit()
    except KeyboardInterrupt:
        print('\nInterrupted By Keyboard')
        WebDriver.quit()