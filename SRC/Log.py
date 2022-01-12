import time
from pathlib import Path
from os import getcwd, remove


class Generate:

    def Write(self, error):
        DateTime = self.__GetDateTime()

        LogPath = getcwd() + '/Data/Log/Log.txt'

        with open(LogPath, 'a') as File:
            self.__DeleteLog(LogPath)

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
