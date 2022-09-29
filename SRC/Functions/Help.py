class Help:

    # Function to configure the help function and prepare it for use
    def __init__(self):
        self.Argument = None
        self.commandsFile = None
        self.Communicate = None
        self.AdditionalArgs = None

    def requirements(self):

        requeriments = {
            'CommandExecution': "/help",
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
        if args in self.commandsFile['Active']['/help']['Args'][0].keys():
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
        elif self.Argument == '-c':
            return self.ListCommands()
        elif self.Argument == '-l':
            return self.ListArgs()
        else:
            return False

    # This function is used to function default or if no argument is given
    def Default(self):
        return self.DescribeCommand()

    # ====== The next functions are used to execute the correct orders depending on the argument given ====== #

    # This function gives the description of the command
    def DescribeCommand(self):
        return self.commandsFile['Active']["/help"]['Desc']

    def ListArgs(self):

        List = self.commandsFile['Active']['/help']['Args'][0]

        ListToMessage = [key + ': ' + List[key] for key in List.keys()]

        return ListToMessage

    def ListCommands(self):

        # show problem in terminal if the command is not working properly
        try:
            # get the list of commands
            ListCommands = [*self.commandsFile['Active']]
            # get the description of the commands
            DescripCommands = [self.commandsFile['Active'][key]['Desc'] for key in ListCommands]

            # create a list of the commands and the description, ready to be sent through the message function
            DataToMessage = [f">> {ListCommands[key]} : {DescripCommands[key][0]}" for key in range(len(ListCommands))]

            # send the list of commands and the description through the message function
            return DataToMessage

        except Exception as e:
            print(e)

