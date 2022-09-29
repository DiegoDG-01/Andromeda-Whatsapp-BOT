##############################################
##############################################
##                                          ##
##   _______ _____  ______ _____ _______    ##
##   |______   |   |_____/   |   |______    ##
##   ______| __|__ |    \_ __|__ ______|    ##
##                                          ##
##             Command Manager              ##
##                                          ##
##############################################
##############################################

# Module imported from the main python library
import Log
from re import match
from json import load
from pathlib import Path
from os import getcwd, listdir
from json import JSONDecodeError
from importlib import import_module


class CommandManager:

    # (InterfaceController) Interface instance to control the web whatsapp interface
    # this instance is only used to some modules
    # Is added from the line #56 and onwards
    def __init__(self, Communicate, InterfaceController, Schedule):

        # Log instance
        self.Log = Log.Generate()

        # List of functions
        self.ListAction = {}

        # Import modules dinamically from the Functions folder
        Modules = self.__import_Modules()

        # Save Communicate to permit communicate with user in whatsapp

        self.arg = None
        self.command = None
        self.commands = None
        self.commandargs = None
        self.commandInfo = None
        self.additionalArgs = {}
        self.Path = Path(getcwd() + '/Data/Config/Codes.json')

        with open(self.Path, 'r') as File:
            try:
                self.commands = load(File)
            except JSONDecodeError as err:
                self.Log.Write("Commands.py | JSONDecodeError # " + str(err))
                exit(1)
            finally:
                File.close()

        # Traverse all modules
        for Module in Modules:

            # Get name of the class splitted by '.'
            ClassName = Module.__name__.split('.')[-1]

            # Get the class from the module
            Module = getattr(Module, ClassName)()

            # Get requirements of the module
            requirements = Module.requirements()
            # Create variable to save list of Extra requirements
            ExternalModules = requirements['ExternalModules']
            # Create variable to save the command to execute the module
            CommandExcecution = requirements['CommandExecution']

            # Check if the module has requirements
            if 'InterfaceController' in ExternalModules:
                Module.set_InterfaceController(InterfaceController)
            if 'Communicate' in ExternalModules:
                Module.set_Communicate(Communicate)
            if 'Schedule' in ExternalModules:
                Module.set_Schedule(Schedule)
            if 'commandsFile' in ExternalModules:
                Module.set_commandFile(self.commands)

            # Generate a dict containing all functions to execute commands
            self.ListAction[CommandExcecution] = Module.EntryPoint


    # Function to import all modules from the Functions folder
    def __import_Modules(self):

        # List of modules
        Functions = []

        # Get all files from the Functions folder
        path = Path(getcwd() + '/Functions/')

        # Get all files from the Functions folder
        for file in listdir(path):
            # Check if the file is a python file and not a folder or a __init__.py
            if not file.startswith("__") and file.endswith(".py"):
                try:
                    # Create name of the module
                    module = 'Functions.' + file[:-3]
                    # Import the module
                    Functions.append(import_module(module))
                except Exception as err:
                    # Log error
                    self.Log.Write("Commands.py | Error importing module " + file + " | " + str(err))
                    exit(1)

        # Return the list of modules imported
        return Functions

    def Get_List_of_Functions(self):
        return self.ListAction


    def Read(self, command):

        """[summary]

        Returns:
            [type]: [description]
        """

        # save command
        self.command = command[0]
        # remove command position
        command.pop(0)
        # save command args
        self.commandargs = command

        if self.__IsCommand():

            IsValid, info = self.__IsValidCommand()

            return IsValid, info
        else:
            return False, None

    def Execute(self):

        if self.commandargs:
            contentargs, error = self.__ContentArgs()

            if contentargs is True and error is None:
                return self.ListAction[self.command](args=self.arg, additionalArgs=self.additionalArgs), None
            else:
                return contentargs, error
        else:
            # return self.ListAction[self.command][2](self.Communicate), None
            return self.ListAction[self.command](), None

    def __IsCommand(self):

        regex = "^/[a-zA-Z0-9]+$"

        isCommand = match(regex, self.command)

        if isCommand is not None:
            return True
        else:
            return False

    def __IsValidCommand(self):

        if self.command in self.commands['Active']:
            self.commandInfo = self.commands['Active'][self.command]
            return True, None
        elif self.command in self.commands['Development']:
            self.commandInfo = self.commands['Development'][self.command]
            return True, "Command in development"
        else:
            return False, 'Invalid command'

    def __ContentArgs(self):

        if self.commandargs:

            if self.commandargs[0] in self.commands['Active'][self.command]["Args"][0].keys():
                self.arg = self.commandargs.pop(0)

                if len(self.commandargs):
                    self.__AdditionalArgs(self.commandargs)

                return True, None
            else:
                return False, "Invalid argument"
        else:
            return False, "Argument not exist"

    def __AdditionalArgs(self, args):

        regex = "^-[a-zA-Z]+$"

        if len(args) % 2 == 0:

            for i in range(0, len(args), 2):

                if match(regex, args[i]) is not None:

                    self.additionalArgs[args[i]] = args[i + 1]
