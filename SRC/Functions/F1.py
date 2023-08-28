import sys
import requests
from json import load
from pathlib import Path
from os import getcwd, environ
from Functions.Base import BaseModule


class F1(BaseModule):

    def __init__(self):
        super().__init__('f1')

        try:
            PathModuleMessages = Path(sys._MEIPASS + '/Data/Modules/Messages/F1.json')
        except Exception:
            PathModuleMessages = Path(getcwd() + '/Data/Modules/Messages/F1.json')

        # API Documentation:
        # https://documenter.getpostman.com/view/11586746/SztEa7bL#46c7fbee-e90f-409f-b2ff-d8b77e85e5f6
        self.API_Url = "http://ergast.com/api/f1/"

        with open(PathModuleMessages, 'r') as file:
            self.ModuleMessages = load(file)
            self.ModuleMessages = self.ModuleMessages[environ['Language']]
            file.close()

    def CommandManager(self):
        if self.Argument == '-d':
            return self.DescribeCommand()
        elif self.Argument == '-l':
            return self.ListArgs()
        elif self.Argument == '-qualify':
            return self.send_request(type='qualifying')
        elif self.Argument == '-race':
            return self.send_request(type='results')
        else:
            return False

    def send_request(self, results=3, limit=20, type='qualifying') -> list:

        URL = self.API_Url + "current/last/" + type + ".json"
        Message = ['']

        if "-r" in self.AdditionalArgs.keys():
            results = int(self.AdditionalArgs['-r'])

        if results > limit:
            results = limit
        elif results < 1:
            results = 1

        try:
            response = requests.get(URL)

            if response.status_code == 200:

                if type == 'qualifying':
                    Message = self.Qualify(response.json(), results)
                elif type == 'results':
                    Message = self.Race(response.json(), results)

            elif response.status_code == 404:
                Message.append('Error: ' + self.ModuleMessages['error']['NotData'])
            elif response.status_code == 503:
                Message.append('Error: ' + self.ModuleMessages['error']['ServiceUnavailable'])
            else:
                Message.append('Error: ' + self.ModuleMessages['error']['Unknown'])

        except Exception as error:
            self.Log.Write("F1.py | GeneralErr # " + str(error))
            Message.append('Error: ' + self.ModuleMessages['error']['Unknown'])

        self.AdditionalArgs = None

        return Message



    def Qualify(self, response, results) -> list:

        Message = ['']

        for i in range(results):
            Message.append(
                '>> ' + str(i+1) + ' - ' + response['MRData']['RaceTable']['Races'][0]['QualifyingResults'][i]['Driver']['code']
            )

        return Message


    def Race(self, response, results) -> list:

        Message = ['',]

        for i in range(results):
            Message.append(
                '>> ' + str(i + 1) + ' - ' + response['MRData']['RaceTable']['Races'][0]['Results'][i]['Driver']['code']
            )

        return Message