import sys
from json import load
from time import sleep
from pathlib import Path
from os import getcwd, environ
from Functions.Base import BaseModule
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GSearch(BaseModule):

    # Function to configure the help function and prepare it for use
    def __init__(self):
        super().__init__('GSearch')

        try:
            PathModuleMessage = Path(sys._MEIPASS + '/Data/Modules/Messages/GSearch.json')
        except Exception:
            PathModuleMessage = Path(getcwd() + '/Data/Modules/Messages/GSearch.json')

        self.SearchBar_Class = 'gLFyf'
        self.SearchBar_XPath = '//*[@id="APjFqb"]'
        self.Google = 'https://www.google.com/'

        with open(PathModuleMessage, 'r') as file:
            self.GSearchMessages = load(file)
            self.GSearchMessages = self.GSearchMessages['messages'][environ['Language']]

            file.close()

    def requirements(self):

        requeriments = {
            'CommandExecution': self.NameModule,
            'ExternalModules': [
                'commandsFile', 'Communicate', 'InterfaceController', 'WebDriver'
            ],
        }

        return requeriments

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

        Box_Links_ID = 'rso'

        for content in WebDriver.find_elements(By.ID, Box_Links_ID):
            Content['Info'].append('# '+ str(cout) + ' - ' + content.find_element(By.TAG_NAME, 'h3').text)
            Content['Links'].append(content.find_element(By.TAG_NAME, 'a'))
            cout += 1

        Content['Info'].append(self.GSearchMessages['info']['cancel'][0])

        return Content

    def __Rollback(self):
        self.InterfaceControl.close_tabs()

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

            return message
        except AssertionError as error:
            self.log.Write("GSearch.py | AssertionError - Invalid value # " + str(error))
            self.InterfaceControl.close_tabs()
            return self.GSearchMessages['error']['invalid_value']
