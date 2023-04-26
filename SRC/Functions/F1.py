import Log
import requests
# import DataBase
from os import getcwd
from json import load
from pathlib import Path

class F1:

    # API Documentation:
    # https://documenter.getpostman.com/view/11586746/SztEa7bL#46c7fbee-e90f-409f-b2ff-d8b77e85e5f6

    # Function to configure the help function and prepare it for use
    def __init__(self):
        self.Argument = None
        self.Communicate = None
        self.commandsFile = None
        self.ModuleMessages = None
        self.AdditionalArgs = None

        self.NameModule = "/f1"
        self.Log = Log.Generate()

        self.API_Url = "http://ergast.com/api/f1/"

        PathModuleMessages = str(Path(getcwd() + '/Data/Modules/Messages/F1.json'))

        with open(PathModuleMessages, 'r') as file:
            self.ModuleMessages = load(file)
            file.close()

    def requirements(self):

        requeriments = {
            # In CommandExecution is necessary define the name that the user will use to call the command
            'CommandExecution': "/f1",
            # In ExternalModules is necessary define the modules necessary to make the module work in the list
            # >> commandsFile: is a dictionary with the commands and the information of the command
            # >> Communicate: is an object that will be used to communicate with the user
            # >> InterfaceController: is an object that will be used to control the web WhatsApp interface
            # >> Schedule: is an object that will be used to control the schedule of the module
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
        if args in self.commandsFile['Active'][self.NameModule]['Args'][0].keys():
            self.Argument = args

            if additionalArgs is not None:
                self.AdditionalArgs = additionalArgs

            return True
        else:
            return False

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
        elif self.Argument == '-qualify':
            return self.send_request(type='qualifying')
        elif self.Argument == '-race':
            return self.send_request(type='results')
        else:
            return False

    # This function is used to function default or if no argument is given
    def Default(self):
        return self.DescribeCommand()

    def DescribeCommand(self):
        return self.commandsFile['Active'][self.NameModule]['Desc']

    def ListArgs(self):

        List = self.commandsFile['Active'][self.NameModule]['Args'][0]

        ListToMessage = [key + ': ' + List[key] for key in List.keys()]

        return ListToMessage

    # ================== The next functions are used to execute the correct orders depend ==================

    def send_request(self, results=3, limit=20, type='qualifying') -> list:

        URL = self.API_Url + "current/last/" + type + ".json"
        Message = ['']

        if "-r" in self.AdditionalArgs.keys():
            results = int(self.AdditionalArgs['-r'])

        if results > limit:
            results = limit
        elif results < 1:
            results = 1

        try:
            response = requests.get(URL)

            if response.status_code == 200:

                if type == 'qualifying':
                    Message = self.Qualify(response.json(), results)
                elif type == 'results':
                    Message = self.Race(response.json(), results)

            elif response.status_code == 404:
                Message.append('Error: ' + self.ModuleMessages['error']['NotData'])
            elif response.status_code == 503:
                Message.append('Error: ' + self.ModuleMessages['error']['ServiceUnavailable'])
            else:
                Message.append('Error: ' + self.ModuleMessages['error']['Unknown'])

        except Exception as error:
            self.Log.Write("F1.py | GeneralErr # " + str(error))
            Message.append('Error: ' + self.ModuleMessages['error']['Unknown'])

        self.AdditionalArgs = None

        return Message



    def Qualify(self, response, results) -> list:

        Message = ['']

        for i in range(results):
            Message.append(
                '>> ' + str(i+1) + ' - ' + response['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['Driver']['code']
            )

        return Message


    def Race(self, response, results) -> list:

        Message = ['',]

        for i in range(results):
            Message.append(
                '>> ' + str(i + 1) + ' - ' + response['MRData']['RaceTable']['Races'][0]['Results'][i]['Driver']['code']
            )

        return Message
