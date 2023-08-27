import sys
import time
from pathlib import Path
from os import getcwd, remove


class Generate:

    def __init__(self):
        try:
            self.LogPath = Path(sys._MEIPASS + '/Data/Log/Log.txt')
        except Exception:
            self.LogPath = Path(getcwd() + '/Data/Log/Log.txt')

    def GetLog(self, lines = None):
        with open(self.LogPath, 'r') as File:

            CompleteLog = File.readlines()

            if len(CompleteLog) <= 0:
                Log = ">> No Logs Found"
            else:
                if(lines != None):
                    Log = CompleteLog[-lines:]
                else:
                    Log = CompleteLog

            File.close()

        return Log

    def Write(self, error):
        DateTime = self.__GetDateTime()

        with open(self.LogPath, 'a') as File:
            self.__DeleteLog(self.LogPath)

            File.write(DateTime + error + '\n')
            File.close()

    def __GetDateTime(self):
        tm = time.localtime()
        current_time = time.strftime("[%d/%m/%y][%H:%M:%S] # ", tm)

        return current_time

    def __DeleteLog(self, PathLog):
        FileSize = Path(r'{}'.format(PathLog)).stat().st_size

        if FileSize > 20000:
            remove(PathLog)
