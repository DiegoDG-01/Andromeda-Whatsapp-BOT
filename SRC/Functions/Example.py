######################################################################################
######################################################################################
##                                                                                  ##
##   /$$$$$$$$                                             /$$                      ##
##  | $$_____/                                            | $$                      ##
##  | $$       /$$   /$$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$ | $$  /$$$$$$             ##
##  | $$$$$   |  $$ /$$/ |____  $$| $$_  $$_  $$ /$$__  $$| $$ /$$__  $$            ##
##  | $$__/    \  $$$$/   /$$$$$$$| $$ \ $$ \ $$| $$  \ $$| $$| $$$$$$$$            ##
##  | $$        >$$  $$  /$$__  $$| $$ | $$ | $$| $$  | $$| $$| $$_____/            ##
##  | $$$$$$$$ /$$/\  $$|  $$$$$$$| $$ | $$ | $$| $$$$$$$/| $$|  $$$$$$$            ##
##  |________/|__/  \__/ \_______/|__/ |__/ |__/| $$____/ |__/ \_______/            ##
##                                              | $$                                ##
##                                              | $$                                ##
##                                              |__/                                ##
##                                                                                  ##
######################################################################################
######################################################################################

# Version: 1.1
# Compatibility: Andromeda >= 0.1.3

# >> THIS FILE IS ONLY THE STRUCTURE OF THE MODULE <<
# >> DO NOT ADD CODE HERE, COPY IT TO YOUR OWN MODULE <<
# >> DO NOT EDIT THE FUNCTION NAMES <<
# >> DO NOT EDIT THE FUNCTION PARAMETERS <<
# >> FOR MORE INFORMATION ON FUNCTIONS, READ THE DOCUMENTATION IN DOCS/DEVELOPER_MODULE.md <<

class Example:

    # Function to configure the help function and prepare it for use
    def __init__(self):
        self.Argument = None
        self.commandsFile = None
        self.Communicate = None

    def requirements(self):

        requeriments = {
            # In CommandExecution is necessary define the name that the user will use to call the command
            'CommandExecution': "/example",
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

    ###################################################################################################################
    ## >> The next functions is used to configure the module                                                        ##
    ## >> The name of the function must be identical, the order are not important                                   ##
    ## >> Copy only the code of the function you want to use                                                        ##
    ###################################################################################################################
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

    ###################################################################################################################
    ## >> The previus functions is used to configure the module                                                      ##
    ## >> The name of the function must be identical, the order are not important                                   ##
    ## >> Copy only the code of the function you want to use                                                        ##
    ###################################################################################################################

    ###################################################################################################################
    ## >> The next is required to execute the module correctly                                                       ##
    ## >> The functions is basically to correctly work with the bot                                                  ##
    ## >> Copy all code in your file                                                                                 ##
    ###################################################################################################################
    # Function to prepare info to argument
    def __PrepareArgs(self, args):
        if args[0] in self.commandsFile['Active']['/help']['Args'][0].keys():
            self.Argument = args[0]
            return True
        else:
            return False

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
        else:
            return False

    ###################################################################################################################
    ## >> The previous is required to execute the module correctly                                                   ##
    ## >> The functions is basically to correctly work with the bot                                                  ##
    ## >> Copy all code in your file                                                                                 ##
    ###################################################################################################################

    ###################################################################################################################
    ## >> The next commands are used to manage the basic functions                                                   ##
    ## >> These functions will be found in most module files                                                         ##
    ###################################################################################################################

    # This function is used to function default or if no argument is given
    def Default(self):
        return self.DescribeCommand()

    def DescribeCommand(self):
        return self.commandsFile['Active']["/help"]['Desc']

    def ListArgs(self):

        List = self.commandsFile['Active']['/help']['Args'][0]

        ListToMessage = [key + ': ' + List[key] for key in List.keys()]

        return ListToMessage

    ###################################################################################################################
    ## >> The previous commands are used to manage the basic functions                                               ##
    ## >> These functions will be found in most module files                                                         ##
    ###################################################################################################################

    # ================== The next functions are used to execute the correct orders depend ==================