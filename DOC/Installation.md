## Install Andromeda - WhatsApp Bot

This bot is currently being tested on Mac OS, Linux and Windows, but the installer only works on Unix or derived operating systems and for Windows operating systems an alternative basic installer was developed, or it can be installed manually by following the instructions.

If you want this documentation in Spanish, you can find it [here](Spanish/Installation.md).

## 📕 Requirements

Currently, the bot is compatible with the next's operating systems:

- Windows (only tested on Windows 10)
- Linux (APT package manager required)
- Mac OS Big Sur or later (Brew Package Manager required)

You're need have installed the next's software programs:

- Git
- Google Chrome or Microsoft Edge
- Python 3.8 or later

## 🌐 Supported Browsers

Currently, the bot is tested in the following browsers:

 - Google Chrome 98.X or later
 - Microsoft Edge 115 or later

## 💻 Install

* [Linux Installer](#LinuxInstaller)
* [Windows Installer](#WinInstaller)
* [Docker](#Docker)
* [Manual Installation](#ManualInstallation)

### <a name="LinuxInstaller"></a> Using the installer for Unix/Linux

1. Download the latest version of the bot from the [GitHub Release](https://github.com/DiegoDG-01/Whatsapp_BOT/releases) or using **Git** in your terminal:
    ```
    git clone "https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT.git"
    ```
2. In your terminal open the folder with the bot and run the following command:
    ```
    python3 install.py
    ```
    The installation show progress and important information, please wait until the installation is finished.


3. The installer will request the name chat to used for listen the messages (it's recommend create previously one group with **only you**).


4. The installer will create a new folder with the name "Andromeda-Whatsapp_BOT" in your home directory.


5. Head over to the [Initialize the bot](#InitializeTheBot) section to continue.

### <a name="WinInstaller"></a> Windows installer

1. Download the latest version of the bot from the [GitHub Release](https://github.com/DiegoDG-01/Whatsapp_BOT/releases) or using **Git** in your terminal:
    ```
    git clone "https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT.git"
    ```
2. In your terminal open the folder with the bot and run the following command:
    ```
    python3 windows_install.py
    ```
    The installation show progress and important information, please wait until the installation is finished.


3. The installer will request the name chat to used for listen the messages (it's recommend create previously one group with **only you**).


4. Head over to the [Initialize the bot](#InitializeTheBot) section to continue.

### <a name="Docker"></a> Docker installation

1. Make sure you have Docker installed on your system. If you don't have it installed, you can find the installation instructions [here](https://docs.docker.com/get-docker/).


2. Download the latest version of the bot from the [GitHub Release](https://github.com/DiegoDG-01/Whatsapp_BOT/releases) or using **Git** in your terminal:
    ```
    git clone "https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT.git"
    ```

3. In your editor of code open the file "DockerFile"


4. In the line 9 (**ENV Language English**) select the language you want to use, the current available languages are:

    - English
    - Spanish


5. In the line 10 (**ENV Username "ChatName"**) select the name of the chat where you want to listen the messages, it's recommend create previously one group with **only you**.


6. In your terminal open the folder with the bot and run the following command:
    ```
    docker build -t "andromeda" .
    ```
    The installation show progress and important information, please wait until the installation is finished.


7. Head over to the "Initialize the bot" section to continue [here](#InitializeTheBot).

### <a name="ManualInstallation"></a> Manual installation

1. Download the latest version of the bot from the [GitHub Release](


### <a name="ManualInstallation"></a> Manual installation

if you don't want to use the installer.

1. you can download the latest version of the bot from the [GitHub Release](https://github.com/DiegoDG-01/Whatsapp_BOT/releases) or using **Git** in your terminal:
    ```
    git clone "https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT.git"
    ```
2. Copy the folder with the bot to desired location.


3. Open the folder of project


4. (**Optional**) Install virtual environment
   ```
    pip3 install virtualenv
    ```
   
5. (**Optional**) Create a virtual environment:
    ```
    virtualenv -p python3 .venv
    ```
   
6. (**Optional**) Activate the virtual environment:
   
    Unix/Linux: 
    ```
    source .venv/bin/activate
    ```

    Windows:
   ```
   .venv\\Scripts\\activate.bat
   ```

7. inside the folder with the bot, run the following command to install the dependencies:
    ```
    python3 pip install -r requirements.txt
    ```

8. (**Optional Unix/Linux**) In the terminal, run the following command to create alias for the executable easy access,
    "**CHOSEN_PATH**" is the path selected by you in the step 2.
    <br>
    <br>
    if you use Bash:
    ```
    echo 'alias andromeda="cd CHOSEN_PATH/SRC/ && source .venv/bin/activate && python3 entrypoint.py"' >> ~/.bashrc
    ```
    
    if you use ZSH:
    ```
    echo 'alias andromeda="cd CHOSEN_PATH/SRC/ && source .venv/bin/activate && python3 entrypoint.py"' >> ~/.zshrc
    ```
   
9. (**Obligatory**) access to folder **"SRC/Data/Config/Lang"** this folder contains the language files (currently only **English** and **Spanish**) copy ***Codes.json*** and ***Config.json*** and paste them in the root config folder **"SRC/Data/Config"**. 
    ```
    SRC/Data/Config/Codes.json
    SRC/Data/Config/Config.json
    ```
   
10. (**Obligatory**) Open the file **"SRC/Data/Config/Config.json"** and search and replace the value of "**WhatsappName**" this value is name of chat that the bot is reading.
    ```
    "Default": {
            "WhatsappName":"(CHOSEN_NAME)"
            "WhatsappNumber":"",
            "WhatsappGroupName":""
        }
    ```

## <a name="InitializeTheBot"></a> 😎 Initialization

To start the bot, run the next command:

if you created alias for the executable (installer created alias):
```
ANDROMEDA
```

if you didn't create alias ("CHOSEN_PATH" is the path selected by you in Install the step 2)
```
python3 CHOSEN_PATH/SRC/entrypoint.py
```

or if you are using Docker, the first time you run the bot, you need to run the following command to login:
```
docker run -it --name andromeda andromeda
```

if you are logged in, you need to run the following command:
```
docker start andromeda
```

Once started the bot, in the terminal show a QR code to scan and load the session.

<img src="IMG/Whatsapp_Init_Page.png" width="70%">
