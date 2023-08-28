import sys
import psutil
import shutil
from os import getpid
from time import sleep
from pathlib import Path
from dotenv import set_key
from subprocess import call
from os import getcwd, environ
from Functions.Base import BaseModule
from json import load, JSONDecodeError

class Configure(BaseModule):

    def __init__(self):
        super().__init__('config')

        self.ConfigureMessages = None

        try:
            self.PathConfig = Path(sys._MEIPASS + '/Data/Config/Config.json')
            configure_messages_path = Path(sys._MEIPASS + '/Data/Modules/Messages/Configure.json')
        except Exception as error:
            self.PathConfig = Path(getcwd() + '/Data/Config/Config.json')
            configure_messages_path = Path(getcwd() + '/Data/Modules/Messages/Configure.json')

        try:

            with open(self.PathConfig, 'r') as f:
                self.config = load(f)
                self.config = self.config['main']

                f.close()

            with open(configure_messages_path, 'r') as f:
                self.ConfigureMessages = load(f)
                self.ConfigureMessages = self.ConfigureMessages['messages'][environ.get('Language')]

                f.close()

        except JSONDecodeError as error:
            self.log.Write("Configure.py | UnboundLocalError # " + str(error))
            exit(1)

    def CommandManager(self):

        if self.Argument == '-d':
            return self.DescribeCommand()
        elif self.Argument == '-l':
            return self.ListArgs()
        elif self.Argument == '-c':
            return self.Show_Config()
        elif self.Argument == '-L':
            return self.Change_Language()
        else:
            return False

    def Get_Error_Log(self):
        # This function is used to get the error log
        # necessary add permission and users to be implemented
        # Temporary implementation to get the error log
        admin = False

        if (admin == None):
            return "Your are not an admin"
        else:
            return self.log.GetLog(3)

    def Show_Config(self, args=None):
        # This function is used to show the current configuration
        # necessary add permission and users to be implemented
        # Temporary implementation to show the current configuration
        admin = False

        config = ''
        message = []

        try:
            if (admin == None):
                return "Your are not an admin"
            else:
                message.append("Current Configuration: \n")

                for key in self.config.keys():
                    for subkey in self.config[key].keys():
                        config += str(subkey) + ' : ' + str(self.config[key][subkey] + ' | ')

                    config += '\n'

                    message.append(config)

                    config = ''

                return message

        except Exception as error:
            self.log.Write("Configure.py | GenericError # " + str(error))
            return "Error al recuperar la configuración, contacte al administrador o revise el log"

    def Change_Language(self, ):

        Path = getcwd()
        PathLang = Path + '/Data/Config/Lang/'
        Pathdst = Path + '/Data/Config/'
        Language = environ.get('Language')

        Browser_PID = None
        BrowserDriverPID = str(getpid())
        DefaultNameBrowserSystem = environ.get('DefaultBrowser')

        messages = self.ConfigureMessages['set_language']

        try:
            self.Communicate.WriteMessage(messages['change'])
            self.Communicate.SendMessage()

            while True:

                response = self.Communicate.ReadResponse()

                if response == 's' or response == 'y':

                    for process in psutil.process_iter():
                        if DefaultNameBrowserSystem in process.name().lower():
                            Browser_PID = str(process.pid)
                            break

                    if Browser_PID is None:
                        return self.ConfigureMessages['errors']['browser_not_found']

                    self.Communicate.WriteMessage(self.ConfigureMessages['info']['restart'])
                    self.Communicate.SendMessage()

                    if Language == 'Spanish':
                        PathLang = PathLang + 'English/'
                        set_key('.env', 'Language', 'English')

                    elif Language == 'English':
                        PathLang = PathLang + 'Spanish/'
                        set_key('.env', 'Language', 'Spanish')


                    # Copy the new language files to the current directory
                    shutil.copyfile(PathLang + 'Codes.json', Pathdst + 'Codes.json')
                    shutil.copyfile(PathLang + 'Config.json', Pathdst + 'Config.json')

                    sleep(2)

                    call(['python3', 'Reset.py', BrowserDriverPID, Browser_PID])

                    sleep(1)

                elif response == 'n' or response == 'c':
                    self.Communicate.WriteMessage(self.ConfigureMessages['errors']['cancel'])
                    break
                else:
                    sleep(0.2)

            self.Communicate.SendMessage()

        except TypeError as error:
            self.log.Write("Configure.py | TypeError: # " + str(error))
            return self.ConfigureMessages['errors']['generic']

        except Exception as error:
            self.log.Write("Configure.py | GenericError # " + str(error))
            return self.ConfigureMessages['errors']['generic']
