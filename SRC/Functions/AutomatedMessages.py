import re
import Log
import DataBase
from os import getcwd
from json import load
from time import sleep
from hashlib import md5
from pathlib import Path
from random import randint
from datetime import datetime
from json import JSONDecodeError


class AutomatedMessages:

    def __init__(self):

        # It's used to identify the module in the database
        # Not modified this value
        self.ID_Event_In_DB = 1
        self.TableDatabase = 'M_AutomatedMessage'

        self.Data = None
        self.AdditionalArgs = None

        self.DB = DataBase.SQLite()
        self.log = Log.Generate()
        self.Communicate = None
        self.commandsFile = None
        PathModuleMessage = Path(getcwd() + "/Data/Modules/AutomatedMessage.json")

        self.InterfaceControl = None
        self.Schedule = None

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

    def requirements(self):

        requeriments = {
            'CommandExecution': "/AutoMessage",
            'ExternalModules': [
                'commandsFile', 'Communicate', 'InterfaceController', 'Schedule'
            ],
        }

        return requeriments

    def set_Communicate(self, Communicate):
        self.Communicate = Communicate

    def set_commandFile(self, commandsFile):
        self.commandsFile = commandsFile

    def set_InterfaceController(self, InterfaceControl):
        try:
            # This instance is used to control the interface and reset Schedule if needed
            # Not all modules used this functions
            self.InterfaceControl = InterfaceControl
        except Exception as error:
            self.log.Write("Configure.py | InterfaceControl # " + str(error))

    def set_Schedule(self, Schedule):
        try:
            self.Schedule = Schedule
        except Exception as error:
            self.log.Write("Configure.py | Schedule # " + str(error))


    # Function to prepare info to argument
    def __PrepareArgs(self, args, additionalArgs):
        # Check if args is a valid argument

        if args in self.commandsFile['Active']['/AutoMessage']['Args'][0].keys() or args == '-send':
            self.Argument = args

            if additionalArgs is not None:
                self.AdditionalArgs = additionalArgs

            return True
        else:
            # There is an error with not responding  with a message
            # fix this and other modules
            return False

        # this error affects all modules and should be fixed

    # This function is used to initialize the help function
    def EntryPoint(self, args=None, data=None, additionalArgs=None):

        # Validate if passed data to used in other functions and assign it to the variable
        # Data is provided by the Schedule module when the time is reached
        if data is not None:
            self.Data = data

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
        elif self.Argument == '-set':
            return self.Set_Automated_Message()
        elif self.Argument == '-send':
            return self.Send_Message()
        elif self.Argument == '-del':
            return self.Delete_Automated_Message()
        elif self.Argument == '-list':
            return self.Show_List_Messages()
        elif self.Argument == '-edit':
            return self.Edit_Message()
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

    def __List_Automated_Messages(self):

        try:
            List = self.DB.select_data(self.TableDatabase, ['ID_Automation_Module', 'WhatsappName', 'Time', 'Date'])
            count = len(List)

            if List:
                return List
            else:
                return False
        except Exception as error:
            self.log.Write("AutomatedMessages.py | GenErr # " + str(error))

    def __Response_is_digit(self, Response, Min=None, Max=None):

        if Response.isdigit():

            Response = int(Response)

            if Min is not None or Max is not None:
                if Min <= Response or Response <= Max:
                    return True
                else:
                    return False
        else:
            return False

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

        data = ['1', Info["Hash_ID_Automation"], Info['WhatsappName'], Info['Message'], Info['Time'], Info['Date'],
                '-send']

        saved = self.DB.insert_data('M_AutomatedMessage',
                                    ['ID_Type_Event', 'ID_Automation_Module', 'WhatsappName', 'Message', 'Time', 'Date',
                                     'args'], data)

        if saved:

            # ID_TYPE_EVENT = 1
            # This id is used to identify the automated message in the database
            # the value is static and is not changed in the future
            created_automation = self.DB.insert_data('Automation_Event',
                                                     ['ID_Type_Event', 'ID_Automation_Module', 'Status'],
                                                     ['1', ID, '1'])

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

    def Delete_Automated_Message(self):

        try:
            List = self.__List_Automated_Messages()

            if List:
                countList = len(List)

                message = ["# " + str(i) + ": " + List[i][1] + " - " + List[i][2] + " - " + List[i][3] for i in range(countList)]

                message.append("# " + str(countList) + ": Cancel")
                message.append("# Select the number of the message you want to delete")

                self.Communicate.WriteMessage(message)
                self.Communicate.SendMessage()

                while True:
                    selected = self.Communicate.ReadResponse()

                    # Use function to validate
                    if selected is not False:
                        # Validate if the response is a digit using the function __Response_is_digit
                        # 1.- Value to validate
                        # 2.- Min value (optional)
                        # 3.- Max value (optional)
                        if self.__Response_is_digit(selected, 0, countList):
                            selected = int(selected)
                            break
                        else:
                            self.Communicate.WriteMessage('# Invalid option')
                            self.Communicate.SendMessage()

                if 0 <= selected < countList:

                    # Params: 1: Table, 2: Dictionary to Where
                    self.DB.delete_data(self.TableDatabase, {'ID_Automation_Module': List[selected][0]})
                    self.DB.delete_data('Automation_Event', {'ID_Automation_Module': List[selected][0]})

                    self.Schedule.reset_event()

                    return self.AutomatedMessages['success']['Remove']
                else:
                    return self.AutomatedMessages['error']['Remove']
            else:
                return self.AutomatedMessages['error']['NotFound']

        except Exception as error:
            self.log.Write("AutomatedMessages.py | GenErr # " + str(error))

    def Show_List_Messages(self):

        List = self.__List_Automated_Messages()

        if List is not False:

            message = ["# " + str(i) + ": " + List[i][1] + " - " + List[i][2] + " - " + List[i][3] for i in range(len(List))]

            self.Communicate.WriteMessage(message)
            self.Communicate.SendMessage()
        else:
            self.Communicate.WriteMessage(self.AutomatedMessages['error']['NotFound'])
            self.Communicate.SendMessage()

    def Edit_Message(self):

        List = self.__List_Automated_Messages()

        if List:

            message = ["# " + str(i) + ": " + List[i][1] + " - " + List[i][2] + " - " + List[i][3] for i in range(len(List))]

            message.append("# " + str(len(List)) + ": Cancel")
            message.append("# Select the number of the message you want to delete")

            self.Communicate.WriteMessage(message)
            self.Communicate.SendMessage()

            while True:
                selectedMessage = self.Communicate.ReadResponse()

                # Use function to validate
                if selectedMessage is not False:
                    # Validate if the response is a digit using the function __Response_is_digit
                    # 1.- Value to validate
                    # 2.- Min value (optional)
                    # 3.- Max value (optional)
                    if self.__Response_is_digit(selectedMessage, 0, len(List)):
                        selectedMessage = int(selectedMessage)
                        break
                    else:
                        self.Communicate.WriteMessage(['# Invalid option'])
                        self.Communicate.SendMessage()

            if 0 <= selectedMessage < len(List):

                count = 0
                totalKeys = len(self.AutomatedMessages['set'].keys())
                message = ["# What do you want to change?"]


                for key in self.AutomatedMessages['set'].keys():
                    message.append("# " + str(count) + ": " + key)
                    count += 1

                message.append("# " + str(count) + ": Cancel")
                message.append("# Select the number of the field you want to edit")

                self.Communicate.WriteMessage(message)
                self.Communicate.SendMessage()

                while True:
                    selected = self.Communicate.ReadResponse()

                    # Use function to validate
                    if selected is not False:
                        # Validate if the response is a digit using the function __Response_is_digit
                        # 1.- Value to validate
                        # 2.- Min value (optional)
                        # 3.- Max value (optional)
                        if self.__Response_is_digit(selected, 0, totalKeys):
                            selected = int(selected)
                            break
                        else:
                            self.Communicate.WriteMessage(['# Invalid option'])
                            self.Communicate.SendMessage()

                if 0 <= selected < totalKeys:

                    for index, key in enumerate(self.AutomatedMessages['set']):
                        if index == selected:
                            dataToEdit = self.__Get_Info_By_User(self.AutomatedMessages['set'][key]['message'])
                            keyToEdit = key

                            regex = self.AutomatedMessages['set'][key]['regex']

                            if not re.search(regex, dataToEdit):
                                return self.AutomatedMessages['set'][key]['error']['Invalid']

                            break

                    if self.DB.update_data(self.TableDatabase, {keyToEdit: dataToEdit}, {'ID_Automation_Module': List[selectedMessage][0]}):

                        self.Schedule.reset_event()
                        return self.AutomatedMessages['success']['Edit']
                    else:
                        return self.AutomatedMessages['error']['Edit']

                else:
                    return self.AutomatedMessages['error']['Cancel']
            else:
                return self.AutomatedMessages['error']['Cancel']
        else:
            self.Communicate.WriteMessage(self.AutomatedMessages['error']['NotFound'])
            self.Communicate.SendMessage()