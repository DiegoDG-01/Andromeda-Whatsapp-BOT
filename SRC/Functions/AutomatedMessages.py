import re
import Log
import DataBase
from os import getcwd
from json import load
from time import sleep
from hashlib import md5
from datetime import datetime
from random import randint
from json import JSONDecodeError


class AutomatedMessages:

    def __init__(self, commandsFile, Communicate, InterfaceControl, Schedule):

        # It's used to identify the module in the database
        # Not modified this value
        self.ID_Event_In_DB = 2

        self.Data = None

        self.DB = DataBase.SQLite()
        self.log = Log.Generate()
        self.Communicate = Communicate
        self.commandsFile = commandsFile
        PathModuleMessage = getcwd() + "/Data/Modules/AutomatedMessage.json"

        try:
            self.InterfaceControl = InterfaceControl
            self.Schedule = Schedule
        except Exception as error:
            self.log.Write("Configure.py | JSONDecodeError # " + str(error))

        try:

            with open(PathModuleMessage, 'r') as File:
                self.AutomatedMessages = load(File)

                File.close()

        except JSONDecodeError as error:
            self.log.Write("AutomatedMessages.py | JSONDecodeError # " + str(error))
            exit(1)
        except FileNotFoundError as error:
            self.log.Write("AutomatedMessages.py | FileNotFoundError # " + str(error))
            exit(1)

    # Function to prepare info to argument
    def __PrepareArgs(self, args):
        # Check if args is a valid argument

        if not isinstance(args, list):
            args = args.split()

        if args[0] in self.commandsFile['Active']['/AutoMessage']['Args'][0].keys():
            self.Argument = args[0]
            return True
        else:
            # There is an error with not responding  with a message
            # fix this and other modules
            return False

        # this error affects all modules and should be fixed

    # This function is used to initialize the help function
    def EntryPoint(self, args=None, data=None):

        # Validate if passed data to used in other functions and assign it to the variable
        if data is not None:
            self.Data = data

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
        elif self.Argument == '-set':
            return self.Set_Automated_Message()
        elif self.Argument == '-send':
            return self.Send_Message()
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
        return self.commandsFile['Active']["/AutoMessage"]['Desc']

    def ListArgs(self):

        List = self.commandsFile['Active']['/AutoMessage']['Args'][0]

        ListToMessage = [key + ': ' + List[key] for key in List.keys()]

        return ListToMessage

    ###################################################################################################################
    ## >> The previous commands are used to manage the basic functions                                               ##
    ## >> These functions will be found in most module files                                                         ##
    ###################################################################################################################

    # ====== The next functions are used to execute the correct orders depending on the argument given ====== #

    def __Get_Info_By_User(self, Message):

        self.Communicate.WriteMessage(Message)
        self.Communicate.SendMessage()

        while True:
            message = self.Communicate.ReadResponse()

            if message is False:
                sleep(0.2)
            else:
                break

        return message

    def Set_Automated_Message(self):

        # Random ID to identify Automated Message in database
        seed = randint(0, 10000)
        seed = str(seed) + '_' + str(datetime.now())

        # Create hash of the seed and select the 10 characters to use as ID
        ID = md5(seed.encode('utf-8')).hexdigest()[0:20:2]

        Info = {"ID_Type_Event": 2, "Hash_ID_Automation": ID, "WhatsappName": None,
                "Message": None, "Time": None, "Date": None}

        for step in self.AutomatedMessages['set']:
            Info[step] = self.__Get_Info_By_User(self.AutomatedMessages['set'][step]['message'])

            regex = self.AutomatedMessages['set'][step]['regex']

            if not re.search(regex, Info[step]):
                return self.AutomatedMessages['set'][step]['error']['Invalid']

        data = ['1', Info["Hash_ID_Automation"], Info['WhatsappName'], Info['Message'], Info['Time'], Info['Date']]

        saved = self.DB.insert_data('M_AutomatedMessage', ['ID_Type_Event', 'ID_Automation_Module', 'WhatsappName', 'Message', 'Time', 'Date'], data)

        if saved:

            # ID_TYPE_EVENT = 1
            # This id is used to identify the automated message in the database
            # the value is static and is not changed in the future
            created_automation = self.DB.insert_data('Automation_Event', ['ID_Type_Event', 'ID_Automation_Module', 'Status'], ['1', ID, '1'])

            if created_automation:
                self.Schedule.reset_event()
                return self.AutomatedMessages['success']['Set']
            else:
                return self.AutomatedMessages['error']['Set']
        else:
            return self.AutomatedMessages['error']['Set']

    def Send_Message(self):

        """
        This function is used to send a message to a specific user

                Data: List [WhatsappName', 'Date', 'Time', 'Message']
        """

        if self.Data is not None:

            if self.InterfaceControl.change_view(self.Data[0]):

                self.Communicate.WriteMessage(self.Data[1])
                self.Communicate.SendMessage()

                self.InterfaceControl.return_to_bot()

                return self.AutomatedMessages['success']['Send']
            else:
                return self.AutomatedMessages['error']['Send']
        else:
            return ['Error', 'No ID given']
