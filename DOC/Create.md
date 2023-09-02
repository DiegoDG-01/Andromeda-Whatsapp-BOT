## Developing Modules for Andromeda - Whatsapp BOT

Si deseas leer este documento en español, puedes hacerlo [aquí](Spanish/Create.md).

This document explains how to develop a module for Andromeda following the project's required standards.

## 💡 Understanding Module Development

A module consists of three main files:
- The Python file containing the logic.
- The file with the messages that will be sent to the user (errors, successes, information, etc.).
- The file with the module's configuration (Name, description, arguments, or available functions).

## 💬 Creating the Message File

This file is **not obligatory**, but it is recommended to have control over the messages that will be sent to the user. Additionally, if your module is intended to work in multiple languages, this file will be responsible for storing the messages in each language.
<br>

This decision is up to the developer, but it is recommended to create this file.

You will need to create a **json** file with the name of your module `MyModule.json` in the following path:
```bash
SRC/Data/Modules/Messages/MyModule.json
``` 
and within this file, you should place the messages that will be sent to the user, for example:
```json
{
    "error": {
        "no_args": "No necessary arguments have been provided to execute this command.",
        "no_permission": "You do not have permission to execute this command."
    },
    "success": {
        "command_executed": "Command executed successfully."
    },
    "info": {
        "command_info": "This command is an example."
    }
}
```

These messages will be entirely controlled by your module, so you are not obligated to use a structure like the one above, but it is recommended to maintain order in the messages.

**Note:** You can access the language being used in the bot from the environment variable `Language` located in the `.env` file.

```python
from os import environ

lang = environ.get('Language')
```

## ⚙️ Creating the Configuration File

You should create a **json** file with the name of your module `MyModule.json` in the following path:

```bash
SRC/Data/Modules/Codes/MyModule.json
```

This file is responsible for storing the configuration of the module, including the necessary name for calling it, description, arguments, functions, etc.

This file should have the following structure:

```json
{
  "English": {
    "/MyModule": {
      "Desc": [
        "Description of the module"
      ],
      "Args": [
        {
          "-d": "Command Description",
          "-l": "List command arguments",
          "-arg": "function of the module"
        }
      ]
    }
  },
  "Spanish": {
    "/MyModule": {
      . . . 
    }
  }
}
```

**Important:** The module's name must be the same as the name of the Python file that contains the module's logic.

- **English**: This is the language in which the module's configuration is written, in this case, it's English.
- **/MyModule**: This is the name of the module, and it will be used to locate the module internally.
- **Desc**: This is the module's description, and it will be displayed to the user when they execute the command `/mymodule_name` or `/mymodule_name -d`.
- **Args**: This is the list of arguments that the module will have. These arguments will be used to execute the module's functions. For example: `/mymodule_name -arg`. It can contain **n** arguments depending on the functions the bot will perform.

The following arguments are mandatory:
- **-d**: This argument will be used to list the available arguments of the module. This argument is mandatory for the module to be executed.
- **-l**: This argument will be used to list the available arguments of the module. This argument is mandatory for the module to be executed.

**Note:** It is mandatory for the configuration file to follow the same pattern as the example above.

**Note #2:** The need for having a `Lang` object in the configuration file has been removed. Now, the default language that the module will use is the one specified in the bot's configuration file located in its .env file at the root of the project. Set the languages as keys in the configuration file. If the language is entirely different from the bot's default language, set the key as **Default**, and it won't matter what language is specified in the bot's configuration.

```json
{
  "Default": {
    . . .
  }
}
```

## 🐍 Creating the Python File

In the following path, you will find a file named `Base.py`. This file contains the basic functions that a module must have to work correctly. So, you should import this file into your module for it to function properly.

```bash
SRC/Functions/Base.py
```

### 📝 Basic Functions

This is a brief explanation of the functions contained in the `Base.py` file and their implementation for proper functioning.

#### 📌 __init__

In this section, the module's name is set in the `self.NameModule` variable.

```python
self.NameModule = f"/{self.NameModule}"
```

**Note:** This name must be unique and cannot coincide with the name of any other module. Additionally, it must be identical to the key in the configuration file.

#### 📌 requirements

```python
def requirements(self):
    requeriments = {
        'CommandExecution': self.NameModule,
        'ExternalModules': [
            'commandsFile', 'Communicate'
        ],
        'Dependencies': {
            'Whisper':'0.2.0'
        }
    }
    return requeriments
```
This function is responsible for defining the module's requirements. In this case, it defines that the execution command from WhatsApp should be the same as the module's name, and the required modules are `commandsFile` and `Communicate`. Additionally, there are other external modules that can be used, which are:

- `commandsFile` - **(Mandatory)** Allows access to the list of module execution commands.
- `Communicate` - **(Mandatory)** Allows writing and sending messages using the WhatsApp chat.
- `InterfaceController:` - Allows obtaining the browser instance to interact with the browser's interface and use it outside of WhatsApp.
- `Schedule:` - Allows scheduling tasks to run at specific times.

Dependencies are a dictionary that contains the external modules required for the module to function correctly. In this case, the module `Whisper` in version `0.2.0` is needed. If there are no dependencies, this section can be omitted.

**Important:** This function can be overridden from the module's file to add more modules or dependencies.

#### 📌 set_commands


```python
    def set_Communicate(self, Communicate):

    def set_commandFile(self, commandsFile):

    def set_InterfaceController(self, InterfaceControl):

    def set_Schedule(self, Schedule):
```

These functions are responsible for receiving the instances of external modules defined in the `requirements` function and storing them in variables for use in the module.

#### 📌 CommandManager

```python
  def CommandManager(self):
    if self.Argument == '-d':
        return self.DescribeCommand()
    elif self.Argument == '-l':
        return self.ListArgs()
    else:
        return False
```
This function is responsible for managing the commands executed from WhatsApp. In this case, two commands are defined: `-d` and `-l`. These commands are mandatory functions for the module to be executed with the basic functions.

It can be overridden from the module's file to add more commands but keeping the `-d` and `-l` commands to ensure that the module can be executed.

### 🧑🏻‍💻 Creating Our Module

Now that we understand how the `Base.py` file works, we can create our module.

To create it, we should generate a file with the name of our module `MyModule.py` in the following path:
```bash 
SRC/Modules/MyModule.py
```

Now, we should import the `Base.py` file, create a class for our module, inherit from the `BaseModule` class, and pass the name of our module as a parameter to the parent class.
```python
from Functions.Base import BaseModule

class MyModule(BaseModule):

    def __init__(self):
        # Inicializamos la clase padre y le pasamos el de nuestro módulo
        super().__init__("MyModule")
```

If our module requires other external modules, we should override the `requirements` function and add the modules we need. For example:
```python
def requirements(self):
    requeriments = {
        'CommandExecution': self.NameModule,
        'ExternalModules': [
            'commandsFile', 'Communicate', 'InterfaceController'
        ],
        'Dependencies': {
            'Whisper':'0.2.0',
            'ChatGPT':'0.1.0' 
        }
    }
    return requeriments
```

We should also override the `CommandManager` function to add the commands we need. For example:

```python
  def CommandManager(self):
    if self.Argument == '-d':
        return self.DescribeCommand()
    elif self.Argument == '-l':
        return self.ListArgs()
    elif self.Argument == '-arg':
        return self.MyNewFunction()
    elif self.Argument == '-arg2':
        return self.MyNewFunction2()
    else:
        return False
```

From here onwards, you can create the functions you need for your module. For example:

```python
    def MyNewFunction(self):
        self.Communicate.WriteMessage("Hello World")
        self.Communicate.SendMessage()
        return True
```

Make sure that the function is present both in the `configurations` file and within the `CommandManager` function so that it can be executed.

## 🏃🏽‍♂️ Running the Module

Start the bot, and it will automatically load the module.

If any issues occur with the module, navigate to the `Logs` folder and check the `Log.txt` file for possible errors.

```bash
SRC/Data/Log/Log.txt
```

#### 💬 Calling the Module

Navigate to your WhatsApp application and type the module's execution command, for example: `/mymodule_name`