from Functions.Base import BaseModule

class Help(BaseModule):
    def __init__(self):
        super().__init__('help')

    def CommandManager(self):
        if self.Argument == '-d':
            return self.DescribeCommand()
        elif self.Argument == '-c':
            return self.ListCommands()
        elif self.Argument == '-l':
            return self.ListArgs()
        else:
            return False

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
            self.log.Write("Help.py | GeneralErr # " + str(e))
