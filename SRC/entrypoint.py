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
import Log
import Config
from os import getcwd
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def InitWebDriver():
    """[summary]

    Returns:
        [type]: [description]
    """

    URL = 'https://web.whatsapp.com/'

    PathSession = getcwd() + '/Data/Session/'

    PathDownloads = str(Path(getcwd() + '/Data/WhatsApp/Downloads/'))
    prefs = {
        "download.default_directory": PathDownloads,
        "directory_upgrade": True
    }

    _Chrome_options = Options()
    _Chrome_options.add_argument('--user-data-dir=' + PathSession)
    _Chrome_options.add_argument('--disable-extensions')
    _Chrome_options.add_argument('--disable-dev-shm-usage')
    _Chrome_options.add_argument('--no-sandbox')
    _Chrome_options.add_argument('--window-size=1920x1080')
    _Chrome_options.add_argument('--start-maximized')
    _Chrome_options.add_experimental_option("prefs", prefs)

    # Hide the browser window
    _Chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36')
    _Chrome_options.add_argument('--headless')

    try:
        WebDriver = Chrome(options=_Chrome_options, service=Service(ChromeDriverManager().install()))
        WebDriver.get(URL)

        return WebDriver
    except Exception as error:
        Log.Write("entrypoint.py # " + str(error))
        WebDriver.quit()


if __name__ == '__main__':

    Log = Log.Generate()

    try:

        # Initialize WebDriver connection
        WebDriver = InitWebDriver()

        # Initialize Bot and pass WebDriver to get access to the browser
        Bot = Bot.Bot(WebDriver)
        # Initialize Config and pass WebDriver to get access to the browser
        Config = Config.Config(WebDriver)

        # Welcome message
        Welcome = Config.GetWelcome()

        # Seter the welcome message
        Bot.SetWelcomeMessage(Welcome)

        # Start Configurator
        if Config.Initialize():
            # Start Bot
            Bot.ReadMessage(WebDriver)
        else:
            print(Config.GetError())  # Get the error to debug
            # if Configurator is not initialized and occurs an error save the error in the log
            Log.Write("Entrypoint # " + str(Config.GetError()))

        # is ended the program, close the WebDriver
        WebDriver.quit()

    # if occurs an error save the error in the log
    except UnboundLocalError as error:
        Log.Write("entrypoint.py | UnboundLocalError # " + str(error))
    except TypeError as error:
        Log.Write("entrypoint.py | TypeError # " + str(error))
    except KeyboardInterrupt:
        # if the user press Ctrl+C, close the WebDriver
        WebDriver.quit()
    except Exception as error:
        Log.Write("entrypoint.py # " + str(error))
        WebDriver.quit()
