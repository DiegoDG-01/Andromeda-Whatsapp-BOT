import Log

class Tabs:

    def __init__(self, WebDriver):
        self.WebDriver = WebDriver
        self.Log = Log.Generate()
        # Main Tab is the tab that is openned when the bot is started
        # Forever this tab is openned and is the number 0
        self.Main_Tab = 0
        self.Active_Tab = 0
        # Save the number of tabs openned
        # Note: The number of tabs openned is the number of tabs is 1 but
        # in the windows_handles init in position 0
        # Remember: If you want to know the number of tabs openned this variable and restart 1
        self.Count_Tabs = len(self.WebDriver.window_handles)
        self.Dict_tabs = {}

        # Create a dictionary to save the tabs and mantain the order
        try:
            self.Dict_tabs[self.Main_Tab] = self.WebDriver.current_url
        except Exception as e:
            self.Log.Write("Tabs.py | Error # " + str(e))
            return False

    def active_tab(self):
        return self.Active_Tab

    def open(self, URL):
        try:
            self.WebDriver.execute_script(f"window.open('{URL}', '_blank');")
            self.Dict_tabs[len(self.WebDriver.window_handles) - 1] = URL
            self.Count_Tabs += 1
            return True
        except Exception as e:
            self.Log.Write("Tabs.py | Open Error # " + str(e))
            return False

    # if not pass the number of tab use the main tab
    # if pass the number of tab use the tab that is openned
    def move_tab(self, position=0):
        try:
            # Count_tabs is the number of tabs openned and restart 1 but the list init in position 0
            # Error if you try to move a tab that is not openned
            if position <= self.Count_Tabs or position == 0:
                self.WebDriver.switch_to.window(self.WebDriver.window_handles[position])
                self.Active_Tab = position
                return True
            else:
                self.Log.Write("Tabs.py | Index Error # " + str(f"The position '{position}' is out of range in the list of tabs"))
                return False
        except Exception as e:
            self.Log.Write("Tabs.py | Move Error # " + str(e))
            return False

    def close_tab(self, ID=None):

        list_to_delete = []

        try:
            if len(self.Dict_tabs) > 1:
                if ID is None:
                    for tab in self.Dict_tabs:
                        if tab != self.Main_Tab:
                            self.WebDriver.switch_to.window(self.WebDriver.window_handles[tab])
                            self.WebDriver.close()
                            self.Count_Tabs -= 1
                            list_to_delete.append(tab)
                else:
                    self.WebDriver.switch_to.window(self.WebDriver.window_handles[ID])
                    self.WebDriver.close()
                    self.Count_Tabs -= 1
                    del self.Dict_tabs[ID]

                for tab in list_to_delete:
                    del self.Dict_tabs[tab]

                self.WebDriver.switch_to.window(self.WebDriver.window_handles[self.Main_Tab])

            return True
        except Exception as e:
            self.Log.Write("Tabs.py | Close Error # " + str(e))
            return False