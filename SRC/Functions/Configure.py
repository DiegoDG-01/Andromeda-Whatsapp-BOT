import Log
import psutil
import shutil
from json import load
from time import sleep
from pathlib import Path
from dotenv import set_key
from subprocess import call
from json import JSONDecodeError
from os import getcwd, getpid, environ


class Configure:

    def __init__(self):
        self.PathConfig = Path(getcwd() + '/Data/Config/Config.json')
        self.Argument = None
        self.log = Log.Generate()
        self.Communicate = None
        self.commandsFile = None
        self.AdditionalArgs = None
        self.ConfigureMessages = None

        configure_messages_path = Path(getcwd() + '/Data/Modules/Messages/Configure.json')

        try:

            with open('Data/Config/Config.json', 'r') as f:
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

    def requirements(self):

        requeriments = {
            'CommandExecution': "/config",
            'ExternalModules': [
                'commandsFile', 'Communicate'
            ],
        }

        return requeriments

    def set_Communicate(self, Communicate):
        self.Communicate = Communicate

    def set_commandFile(self, commandsFile):
        self.commandsFile = commandsFile

    # Function to prepare info to argument
    def __PrepareArgs(self, args, additionalArgs):
        if args in self.commandsFile['Active']['/config']['Args'][0].keys():
            self.Argument = args

            if additionalArgs is not None:
                self.AdditionalArgs = additionalArgs

            return True
        else:
            # There is an error with not responding  with a message
            # fix this and other modules
            return False

        # this error affects all modules and should be fixed
        #

    # This function is used to initialize the help function
    def EntryPoint(self, args=None, additionalArgs=None):
        # if args is empty or None execute default function else execute different function depending on the args
        if args is None:
            return self.Default()
        else:
            # check if args exist and is a valid argument
            if self.__PrepareArgs(args, additionalArgs):
                # Execute the function in charge of managing the help function
                return self.CommandManager()
            else:
                return False

    # This function is used to function to management of the help functions and execute the correct function
    def CommandManager(self):

        if self.Argument == '-d':
            return self.DescribeCommand()
        elif self.Argument == '-l':
            return self.ListArgs()
        elif self.Argument == '-log':
            return self.Get_Error_Log()
        elif self.Argument == '-c':
            return self.Show_Config()
        elif self.Argument == '-L':
            return self.Change_Language()
        else:
            return False

    ###################################################################################################################
    ## >> The next commands are used to manage the basic functions                                                   ##
    ## >> These functions will be found in most module files                                                         ##
    ###################################################################################################################

    # This function is used to function default or if no argument is given
    def Default(self):
        return self.DescribeCommand()

    def DescribeCommand(self):
        return self.commandsFile['Active']["/config"]['Desc']

    def ListArgs(self):

        List = self.commandsFile['Active']['/config']['Args'][0]

        ListToMessage = [key + ': ' + List[key] for key in List.keys()]

        return ListToMessage

    ###################################################################################################################
    ## >> The previous commands are used to manage the basic functions                                               ##
    ## >> These functions will be found in most module files                                                         ##
    ###################################################################################################################

    # ====== The next functions are used to execute the correct orders depending on the argument given ====== #

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

