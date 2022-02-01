import Log
import psutil
import shutil
from json import load
from time import sleep
from subprocess import call
from os import getcwd, getpid
from json import JSONDecodeError

class Configure:

    def __init__(self, commandsFile, Communicate):
        self.PathConfig = getcwd() + '/Data/Config/Config.json'
        self.Argument = None
        self.log = Log.Generate()
        self.Communicate = Communicate
        self.commandsFile = commandsFile

        try:

            with open('Data/Config/Config.json', 'r') as f:
                self.config = load(f)
                self.config = self.config['main']

                f.close()

        except JSONDecodeError as error:
            self.log.Write("Configure.py | UnboundLocalError # "+ str(error))
            exit(1)

    # Function to prepare info to argument
    def __PrepareArgs(self, args):
        if args[0] in self.commandsFile['Active']['/config']['Args'][0].keys():
            self.Argument = args[0]
            return True
        else:
            # There is an error with not responding  with a message
            # fix this and other modules
            return False

        # this error affects all modules and should be fixed
        #

    # This function is used to initialize the help function
    def EntryPoint(self, args=None):
        # if args is empty or None execute default function else execute different function depending on the args
        if args is None:
            return self.Default()
        else:
            # check if args exist and is a valid argument
            if self.__PrepareArgs(args):
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
        admin = True

        if(admin == None):
            return "Your are not an admin"
        else:
            return self.log.GetLog(3)

    def Show_Config(self, args = None):
        # This function is used to show the current configuration
        # necessary add permission and users to be implemented
        # Temporary implementation to show the current configuration
        admin = True

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
            self.log.Write("Configure.py | GenericError # "+ str(error))
            return "Error al recuperar la configuración, contacte al administrador o revise el log"


    def Change_Language(self,):


        Path = getcwd()
        PathLang = Path + '/Data/Config/Lang/'
        Pathdst = Path + '/Data/Config/'

        with open(self.PathConfig, 'r') as file:
            Language = load(file)
            Language = Language['config']['language']

            file.close()

        ChromeDriverPID = str(getpid())
        Google_Chrome_PID = None

        Messages = {'Spanish': [f'Tú idioma actual es: {Language}', 'Deseas cambiarlo a inglés? (s/n)', 'Idioma cambiado a inglés',
                          'Error al cambiar el idioma'],
                   'English': [f'Your current language is: {Language}', 'Do you want to change it to spanish? (y/n)',
                          'Language changed to english', 'Error changing language']
                   }

        response = Messages[Language]

        try:
            for step in range(len(Messages[Language])):

                self.Communicate.WriteMessage(Messages[Language][step])
                self.Communicate.SendMessage()

                if(step == 1):

                    while (True):

                        response = self.Communicate.ReadResponse()

                        if(response == 's' or response == 'y'):

                            for process in psutil.process_iter():
                                if 'Google Chrome' in process.name():
                                    if process.name() == 'Google Chrome':
                                        Google_Chrome_PID = str(process.pid)

                            self.Communicate.WriteMessage(['#######################################', '>> El navegador se reiniciara para aplicar los cambios', '#######################################'])
                            self.Communicate.SendMessage()

                            if Language == 'Spanish':
                                PathLang = PathLang + 'English/'
                                pass
                            elif Language == 'English':
                                PathLang = PathLang + 'Spanish/'
                                pass

                            # Copy the new language files to the current directory
                            shutil.copyfile(PathLang+'Codes.json', Pathdst + 'Codes.json')
                            shutil.copyfile(PathLang + 'Config.json', Pathdst + 'Config.json')

                            sleep(2)

                            call(['python3', 'Reset.py', ChromeDriverPID, Google_Chrome_PID])

                            sleep(1)

                        elif(response == 'n' or response == 'c'):
                            self.Communicate.WriteMessage(Messages[Language][3])
                            break
                        else:
                            sleep(0.2)

                    self.Communicate.SendMessage()
                    break

        except Exception as error:
            self.log.Write("Configure.py | GenericError # "+ str(error))
            return "Error al cambiar el idioma, contacte al administrador o revise el log"

        except TypeError as error:
            self.log.Write("Configure.py | TypeError: # "+ str(error))
            return "Error al cambiar el idioma, contacte al administrador o revise el log"