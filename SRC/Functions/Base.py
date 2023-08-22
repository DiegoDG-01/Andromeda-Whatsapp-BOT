import Log


class BaseModule:

    # Function to configure the help function and prepare it for use
    def __init__(self, module_name):
        self.Argument = None
        self.Communicate = None
        self.commandsFile = None
        self.AdditionalArgs = None
        self.NameModule = f"/{module_name}"

        self.log = Log.Generate()

    def set_Communicate(self, Communicate):
        self.Communicate = Communicate

    def set_commandFile(self, commandsFile):
        self.commandsFile = commandsFile

    def set_InterfaceController(self, InterfaceControl):
        try:
            self.InterfaceControl = InterfaceControl
        except Exception as error:
            self.log.Write("Configure.py | InterfaceControl # " + str(error))

    def set_Schedule(self, Schedule):
        try:
            self.Schedule = Schedule
        except Exception as error:
            self.log.Write("Configure.py | Schedule # " + str(error))

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

    # This function is used to function default or if no argument is given
    def Default(self):
        return self.DescribeCommand()

    def DescribeCommand(self):
        return self.commandsFile['Active'][self.NameModule]['Desc']

    def ListArgs(self):

        List = self.commandsFile['Active'][self.NameModule]['Args'][0]

        ListToMessage = [key + ': ' + List[key] for key in List.keys()]

        return ListToMessage
