import Log
from os import getcwd
from json import load
from time import sleep
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GSearch:

    # Function to configure the help function and prepare it for use
    def __init__(self):
        self.Argument = None
        self.commandsFile = None
        self.Communicate = None
        self.NameModule = "/GSearch"
        self.SearchBar_Class = 'gLFyf'
        self.SearchBar_XPath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'
        self.Google = 'https://www.google.com/'
        PathModuleMessage = Path(getcwd() + "/Data/Modules/GSearch.json")

        self.log = Log.Generate()
        self.GSearchMessages = self.__Load_MultiLanguage(PathModuleMessage)

    def requirements(self):

        requeriments = {
            'CommandExecution': "/GSearch",
            'ExternalModules': [
                'commandsFile', 'Communicate', 'InterfaceController', 'WebDriver'
            ],
        }

        return requeriments

    def set_Communicate(self, Communicate):
        self.Communicate = Communicate

    def set_commandFile(self, commandsFile):
        self.commandsFile = commandsFile

    def set_InterfaceController(self, InterfaceControl):
        try:
            self.InterfaceControl = InterfaceControl
        except Exception as error:
            self.log.Write("Configure.py | InterfaceControl # " + str(error))

    def set_WebDriver(self, WebDriver):
        self.WebDriver = WebDriver

    def __Load_MultiLanguage(self, Path):
        try:
            with open(Path, 'r') as file:
                file = load(file)
                default_code = file['lang']['default']
                language_code = file['lang'][default_code]['locale']
                return file['messages'][language_code]
        except Exception as error:
            self.log.Write("GSearch.py | __Load_MultiLanguage # " + str(error))
            return False

    # Function to prepare info to argument
    def __PrepareArgs(self, args):
        if args[0] in self.commandsFile['Active'][self.NameModule]['Args'][0].keys():
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
        elif self.Argument == '-s':
            return self.Search()
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

    def __readMessage(self):
        while True:
            search = self.Communicate.ReadResponse()
            if search != False:
                break
            sleep(0.5)

        return search

    def __CountLinks(self, WebDriver):
        cout = 1
        Content = {
            'Info': [],
            'Links': [],
        }
        Box_Links_Class = 'tF2Cxc'

        for content in WebDriver.find_elements(By.CLASS_NAME, Box_Links_Class):
            Content['Info'].append('# '+ str(cout) + ' - ' + content.find_element(By.TAG_NAME, 'h3').text)
            Content['Links'].append(content.find_element(By.TAG_NAME, 'a'))
            cout += 1

        Content['Info'].append(self.GSearchMessages['info']['cancel'][0])

        return Content

    def __Rollback(self):
        pass

    def Search(self):
        self.Communicate.WriteMessage(self.GSearchMessages['info']['search'])
        self.Communicate.SendMessage()
        search = self.__readMessage()

        try:
            # when create new window automatically open the new tab
            if not self.InterfaceControl.create_new_window(self.Google):
                self.__Rollback()
                return self.GSearchMessages['error']['open_tab']
            if not self.InterfaceControl.move_next_tab():
                self.__Rollback()
                return self.GSearchMessages['error']['move_tab']
        except Exception as error:
            self.log.Write("GSearch.py | InterfaceControl # " + str(error))

        # Get temporarily the WebDriver to custom managment the interface
        TempWebDriver = self.InterfaceControl.get_WebDriver()

        try:
            SearchBar = WebDriverWait(TempWebDriver, 5).until(EC.element_to_be_clickable((By.XPATH, self.SearchBar_XPath)))
            SearchBar.click()
            SearchBar.send_keys(search + Keys.ENTER)
        except Exception as error:
            self.log.Write("GSearch.py | WebDriver # " + str(error))
            self.__Rollback()
            return self.GSearchMessages['error']['search']

        links = self.__CountLinks(TempWebDriver)

        self.InterfaceControl.return_to_main_tab()

        sleep(0.1)

        self.Communicate.WriteMessage(links['Info'])
        self.Communicate.SendMessage()

        page_to_search = self.__readMessage()

        try:
            assert page_to_search == 'exit' or page_to_search.isdigit()

            if page_to_search == 'exit':
                self.InterfaceControl.close_tabs()
                return self.GSearchMessages['info']['cancelled']

            if int(page_to_search) < 1 or int(page_to_search) > len(links['Links']):
                self.InterfaceControl.close_tabs()
                return self.GSearchMessages['error']['index_out_of_range']

            self.Communicate.WriteMessage(self.GSearchMessages['info']['wait'])
            self.Communicate.SendMessage()

            self.InterfaceControl.move_next_tab()
            links['Links'][int(page_to_search) - 1].click()
            image_name = self.InterfaceControl.take_screenshot()
            self.InterfaceControl.return_to_main_tab()

            result, message = self.InterfaceControl.send_mediafile(image_name)

            self.InterfaceControl.close_tabs()

            return [message]
        except AssertionError as error:
            self.log.Write("GSearch.py | AssertionError - Invalid value # " + str(error))
            self.InterfaceControl.close_tabs()
            return self.GSearchMessages['error']['invalid_value']
