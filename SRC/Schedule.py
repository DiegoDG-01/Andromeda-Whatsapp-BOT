###############################################
##                                           ##
##    █████╗ ███████╗██╗███████╗ █████╗      ##
##    ██╔══██╗╚══███╔╝██║╚══███╔╝██╔══██╗    ##
##    ███████║  ███╔╝ ██║  ███╔╝ ███████║    ##
##    ██╔══██║ ███╔╝  ██║ ███╔╝  ██╔══██║    ##
##    ██║  ██║███████╗██║███████╗██║  ██║    ##
##    ╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  ╚═╝    ##
##                                           ##
##                  SCHEDULE                 ##
###############################################

import Log
import schedule
import DataBase
import threading
from time import sleep


class Schedule:

    def __init__(self, list_action):
        self.Events = {}
        self.Log = Log.Generate()
        self.DB = DataBase.SQLite()

        # Is the list to all commands to be executed
        self.ListAction = list_action

        self.consult_database_event()

        if len(self.Events) > 0:
            self.set_event()
            # print(self.get_event())
        else:
            self.Log.Write("Schedule.py | Warning # Not data found in database to enable events")

    def background_set(self, interval=1):

        ThreadBackground = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not ThreadBackground.is_set():
                    schedule.run_pending()
                    sleep(interval)

        ContinuousThread = ScheduleThread()
        ContinuousThread.start()

        return ThreadBackground

    def set_event(self):

        try:
            for event in self.Events:
                if event in self.ListAction.keys():
                    data = self.get_info_to_event(self.Events[event]['ID'])
                    if data is not None:
                        for i in range(len(data)):
                            # the parameters is inside the list because the function waiting for a list
                            schedule.every().days.at(data[i][2]).do(self.ListAction[event], args=['-send'],
                                                                    data=[data[i][0], data[i][1], data[i][2], data[i][3]])

                else:
                    print("Evento no encontrado")
        except TypeError as e:
            self.Log.Write("Schedule.py | TypeError # " + str(e))
        except Exception as e:
            self.Log.Write("Schedule.py | Error # " + str(e))
            # schedule.every().days.at(event[3]).do(self.job, name=event[0], Message=event[1], time=event[3])

    def get_info_to_event(self, id_event):

        """
        This dictionary content the name tables used in the database to get the information
        if add more modules to the system then add the name of the table in the dictionary
        """
        dict_to_get_data = {1: {"table": "M_AutomatedMessage", "data": ['WhatsappName', 'Date', 'Time', 'Message']},
                            2: {"table": "M_Crypto", "data": ['CriptoName', 'Date', 'Time']}
                            }

        if id_event in dict_to_get_data:
            table = dict_to_get_data[id_event]['table']
            data = dict_to_get_data[id_event]['data']

            data = self.DB.select_data(table, data)

            if data is not None:
                return data
            else:
                return None
        else:
            return None

    def get_event(self):
        return self.Events

    def consult_database_event(self):

        query = "SELECT Type_Events.ID, Type_Events.Command, Automation_Event.ID_Automation_Module FROM Type_Events \
                 INNER JOIN Automation_Event ON Type_Events.id = Automation_Event.ID_Type_Event \
                 WHERE Automation_Event.Status = TRUE"

        data = self.DB.custom_query(query)

        # If data is not empty then set the events in the variable Events
        if data is not None:
            ''' 
            ## EXAMPLE OF VARIABLE "EVENTS" STRUCTURE
            >> First key element is the ID of the event in the database
            >> Inside to first dictionary to first key the second key element is the command to be executed
            >> Third key element is the unique id to identified event to be executed
            >> self.Events = {
                '/AutoMessage': {'ID': 1, 'Command': '/AutoMessage', 'ID_Automation_Module': 'HASH_ID_AUTOMATION_MODULE'},
                '/Cripto': {'ID': 2, 'Command': '/Cripto', 'ID_Automation_Module': 'HASH_ID_AUTOMATION_MODULE}}
            '''
            for row in data:
                self.Events[row[1]] = {'ID': row[0], 'Command': row[1], 'ID_Automation_Module': row[2]}
        else:
            # If data is empty then write a log message
            self.Events = None
            self.Log.Write("Schedule.py | Warning # Not data found in database to enable events")
