##############################################
##       __      _____  ___        __       ##
##      /""\    (\"   \|"  \      /""\      ##
##     /    \   |.\\   \    |    /    \     ##
##    /' /\  \  |: \.   \\  |   /' /\  \    ##
##   //  __'  \ |.  \    \. |  //  __'  \   ##
##  /   /  \\  \|    \    \ | /   /  \\  \  ##
## (___/    \___)\___|\____\)(___/    \___) ##
##                                          ##
##       It's a palindrome name  <3         ##  
##                                          ##
##############################################

# Module to control the web whatsapp interface
import InterfaceControl

# Modules to import from the project
import Log
import Commands
import Communicator

# Module imported from the main python library
from time import sleep

# Modules to import from selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Module to check if exists a command automatically
import Schedule


class Bot:

    def __init__(self, WebDriver):

        # Load module Schedule
        # Firts create a new instance of the class schedule to initialize the basic variables
        self.Schedule = Schedule.Schedule()
        # Load Interface Controller
        self.InterfaceControl = InterfaceControl.Interface(WebDriver)
        # Prepare the log to save the messages error
        self.Log = Log.Generate()
        # Prepare the Communicator
        self.Communicate = Communicator.Communicate(WebDriver)
        # Prepare the Commands Manager and pass the Communicator to write and send messages in whatsapp
        # and send the instance schedule to command manager (this instance not contains the action list)
        # the action list is loaded in the function more below
        self.CommandManager = Commands.CommandManager(self.Communicate, self.InterfaceControl, self.Schedule)

        # Load the list of actions in the instance schedule
        # Send list of commands to the module Schedule
        # To execute them automatically
        self.Schedule.init(self.CommandManager.Get_List_of_Functions())
        # This function is used to keep schedule in background and
        # to check if there is a new command to execute
        self.BackgroundSchedule = self.Schedule.background_set()

        # Delete this file the InterfaceControl.Interface object to free memory
        del self.InterfaceControl

    def SetWelcomeMessage(self, Message):
        self.MessageWelcome = [Message[i] for i in Message.keys()]


    def Welcome(self):
        self.Communicate.WriteMessage(self.MessageWelcome)

        if self.Communicate.SendMessage():
            return True

    def ReadMessage(self, WebDriver):

        """[summary]
        """

        ClassGlobalMessageBox = '_3mSPV'

        while True:

            try:
                # Get the message box
                Messages = WebDriver.find_elements_by_class_name(ClassGlobalMessageBox)

                if Messages:

                    # Get the last message
                    Message = Messages.pop().text.split('\n')

                    # Obtiene una lista con el comando y posibles argumentos a ejecutar
                    Message = Message[0].split(" ")

                    # Send the command to the CommandManager
                    Command = self.CommandManager.Read(Message)

                    if Command[0] is True and Command[1] is None:
                        # stop the thread to run the commands in the background and not have a conflict
                        self.BackgroundSchedule.set()

                        ExecutResult, _error = self.CommandManager.Execute()

                        if _error is None:
                            print("Command responded with not error")
                            self.Communicate.WriteMessage(ExecutResult)
                        else:
                            print("Command responded with error")
                            self.Communicate.WriteMessage(_error)

                        if self.Communicate.SendMessage():
                            print("Command responde successfully")
                            sleep(3)

                        # Reactive the thread to run the commands in the background without conflict
                        self.BackgroundSchedule.clear()

                    elif Command[0] is True and Command[1] is not None:

                        self.Communicate.WriteMessage(Command[1])
                        self.Communicate.SendMessage()

                        print("Command responde successfully")
                        sleep(3)

                    # Testing (Delete)
                    elif Command[0] is False and Command[1] is not None:
                        self.Communicate.WriteMessage(Command[1])
                        self.Communicate.SendMessage()

                        print("Command responde successfully")
                        sleep(3)

                    else:
                        print('Reading Message')
                        sleep(1)

                else:
                    print('Reading Message (Empty chat)')
                    if self.Welcome():
                        sleep(1)
                    else:
                        return False

            except TimeoutException as error:
                self.Log.Write("Bot.py # " + str(error))
                return False
            except NoSuchElementException as error:
                self.Log.Write("Bot.py # " + str(error))
                return False