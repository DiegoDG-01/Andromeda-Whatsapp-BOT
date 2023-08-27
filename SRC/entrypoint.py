########################################################
########################################################
##                                                    ##
##           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠒⠒⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀           ##
##           ⠀⠀⠀⠀⠀⢀⣤⣶⡾⠿⠿⠿⠿⣿⣿⣶⣦⣄⠙⠷⣤⡀⠀⠀⠀⠀           ##
##           ⠀⠀⠀⣠⡾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣷⣄⠘⢿⡄⠀⠀⠀           ##
##           ⠀⢀⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠐⠂⠠⢄⡀⠈⢿⣿⣧⠈⢿⡄⠀⠀           ##
##           ⢀⠏⠀⠀⠀⢀⠄⣀⣴⣾⠿⠛⠛⠛⠷⣦⡙⢦⠀⢻⣿⡆⠘⡇⠀⠀           ##
##           ⠀⠀⠀⠀⡐⢁⣴⡿⠋⢀⠠⣠⠤⠒⠲⡜⣧⢸⠄⢸⣿⡇⠀⡇⠀⠀           ##
##           ⠀⠀⠀⡼⠀⣾⡿⠁⣠⢃⡞⢁⢔⣆⠔⣰⠏⡼⠀⣸⣿⠃⢸⠃⠀⠀           ##
##           ⠀⠀⢰⡇⢸⣿⡇⠀⡇⢸⡇⣇⣀⣠⠔⠫⠊⠀⣰⣿⠏⡠⠃⠀⠀⢀           ##
##           ⠀⠀⢸⡇⠸⣿⣷⠀⢳⡈⢿⣦⣀⣀⣀⣠⣴⣾⠟⠁⠀⠀⠀⠀⢀⡎           ##
##           ⠀⠀⠘⣷⠀⢻⣿⣧⠀⠙⠢⠌⢉⣛⠛⠋⠉⠀⠀⠀⠀⠀⠀⣠⠎⠀           ##
##           ⠀⠀⠀⠹⣧⡀⠻⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡾⠃⠀⠀           ##
##           ⠀⠀⠀⠀⠈⠻⣤⡈⠻⢿⣿⣷⣦⣤⣤⣤⣤⣤⣴⡾⠛⠉⠀⠀⠀⠀           ##
##           ⠀⠀⠀⠀⠀⠀⠈⠙⠶⢤⣈⣉⠛⠛⠛⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀           ##
##           ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀           ##
##                                                    ##
##                 Andromeda - WhatsApp               ##
##                                                    #
########################################################
########################################################


import sys
import Bot
import Log
import Config
import SetBrowser
from os import environ
from dotenv import load_dotenv


def InitWebDriver():

    selectBrowser = SetBrowser.Browser()

    URL = 'https://web.whatsapp.com/'

    try:
        WebDriver = selectBrowser.SetBrowser(environ.get('DefaultBrowser'))

        if WebDriver == False:
            return exit(1)

        WebDriver.get(URL)

        return WebDriver
    except Exception as error:
        Log.Write("entrypoint.py # " + str(error))
        WebDriver.quit()


if __name__ == '__main__':

    try:
        # Load the environment variables
        load_dotenv(sys._MEIPASS + '/.env')
    except Exception:
        # Load the environment variables
        load_dotenv()

    Log = Log.Generate()

    try:

        # Initialize WebDriver connection
        WebDriver = InitWebDriver()

        # Initialize Config and pass WebDriver to get access to the browser
        Config = Config.Config(WebDriver)

        # Start Configurator
        if Config.Initialize():
            # Initialize Bot and pass WebDriver to get access to the browser
            Bot = Bot.Bot(WebDriver)

            # Welcome message
            Welcome = Config.GetWelcome()

            # Seter the welcome message
            Bot.SetWelcomeMessage(Welcome)

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
