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

        # List of modules available
        self.AvailableModules = []

        # Dict to save the functions to execute commands
        self.ListAction = {}
        # Convert the dict to a list to use the index of the list as a command
        TempListAction = None

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

        self.TempDependency_Dict = {}

        try:
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

                # save the dependencies of the module to import them later
                if 'Dependencies' in requirements:
                    self.TempDependency_Dict[ClassName] = {
                        # This is the module where it will be imported
                        'Module': Module,
                        # This is the list of dependencies
                        'Dependencies': requirements['Dependencies'],
                    }

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

                # Add dinamically codes of the third party modules to the main codes file "self.commands"
                Codes = self.__import_codes_of_module(ClassName)

                if Codes is not False:
                    self.commands['Active'].update(Codes)

                Modules[self.AvailableModules.index(ClassName)] = Module

            TempListAction = list(self.ListAction.keys())

            # Import dependencies
            for Module in self.TempDependency_Dict: #ChatGPT
                Dependencies_status = True
                Dependencies = self.TempDependency_Dict[Module]['Dependencies'].keys()

                # Check if the dependencies are installed
                for dependency in Dependencies:
                    # Check if the dependency is installed
                    if not dependency in self.AvailableModules:
                        self.Log.Write("Commands.py | Information of modules | Module " + Module + " requires module " + dependency + " to work")
                        self.ListAction.pop(TempListAction[self.AvailableModules.index(Module)])
                        Dependencies_status = False

                # If the dependencies are not installed, skip the module
                if Dependencies_status == False:
                    continue

                for dependency in Dependencies:
                    self.TempDependency_Dict[Module]['Module'].set_dependency(dependency, Modules[self.AvailableModules.index(dependency)])

        except Exception as err:
            self.Log.Write("Commands.py | Error load modules | " + str(err))
            exit(1)

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
                    # Imported module but not initialized
                    Functions.append(import_module(module))
                    # Add the module to the list of available modules
                    self.AvailableModules.append(file[:-3])
                except Exception as err:
                    # Log error
                    self.Log.Write("Commands.py | Error importing module " + file + " | " + str(err))
                    exit(1)

        # Return the list of modules imported
        return Functions

    def __import_codes_of_module(self, NameFile):

        ModuleCodes = Path(getcwd() + '/Data/Modules/Codes/' + NameFile + '.json')

        if ModuleCodes.exists():
            with open(ModuleCodes, 'r') as File:
                try:
                    Module = load(File)
                    lang = Module['Lang']

                    return Module[lang]
                except JSONDecodeError as err:
                    self.Log.Write("Commands.py | JSONDecodeError # " + str(err))
                    exit(1)
                except Exception as err:
                    self.Log.Write("Commands.py | Error importing codes of module " + NameFile + " | " + str(err))
                    exit(1)
        else:
            return False

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
