## Development module for Andromeda - Whatsapp BOT

This file is a guide to developers who want to create their own modules for Andromeda - Whatsapp BOT.

If you want this documentation in Spanish, you can find it [here](../Spanish/Development/Create.md).

## 💡 Understand the structure of the project

The project is divided into 3 main files:
- The python file that contains the code of the module.
- The file for the configuration of the module (Name, description, arguments/functions, etc.).
- The file for the messages of the module (Errors, warnings, success, etc.).

## 💬 Create file of the messages

This files is not obligatory, but it is recommended to use it. This file contains the messages that the module will send to the user. The messages are in JSON format.
<br>

It's decision to developers if they want to use the file or not.

The file it must create with the name of the module and the extension `.json`. For example, `MyModule.json` in the next route: 
```bash
SRC/Data/Modules/Messages/MyModule.json
```
and inside of the file must be a example like this:
```json
{
    "error": {
        "no_args": "No se han proporcionado los argumentos necesarios para ejecutar este comando.",
        "no_permission": "No tienes permisos para ejecutar este comando."
    },
    "success": {
        "command_executed": "Comando ejecutado correctamente."
    },
    "info": {
        "command_info": "Este comando es un ejemplo."
    }
}
```
These messages are used in the module and it is not necessary to use the same names or structure since the developer will be in charge of managing this file.

## ⚙️ Create file of the configuration

This file is **obligatory** because it contains the configuration of the module.

The configuration is in **JSON** format and name of the file must be the name of the module. For example, `MyModule.json` in the next route:
```bash
SRC/Data/Modules/Codes/MyModule.json
```

The configuration must contain the name of module, description, arguments that will be the available functions and languages that will be available for the module.

The file structure should be as follows
```json
{
  "Lang": "English",
  
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
    ...
  }
}
```

- **English**: Is the object that contains the configuration of the module in English.
- **/MyModule**: Is the name of the module. It must be the same as the name of the python file that contains the module logic.
- **Desc**: Is the description of the module and is used to show the description of the module when the user uses the command `/mymodule_name` or `/mymodule_name -d` in Whatsapp.
- **Args**: Is the arguments of the module and can contain **n** arguments.


The following is a obligatory argument and it is used to show the arguments of the module when the user uses the command `/mymodule_name -l` or `/mymodule_name -d` to show description of the module.
- **-d**: Show the description of the module.
- **-l**: List the arguments of the module.

**Note:** it is obligatory that the configuration file follows the same pattern as the previous example.

## 🐍 Create a python file


In the following path you will find a file called `Example.py` which contains the template with the basic functions needed to develop a module.

```bash
SRC/Functions/Example.py
```

Copy the file and rename it with the name of the module. For example, `MyModule.py`.

```bash
SRC/Functions/MyModule.py
```

### 📝 Basic functions

The file must contain the following functions:

#### 📌 __init__

This function is the constructor, and it is used to initialize the class.

In this section you must set the name of the module in the variable `self.NameModule` including the `/` at the beginning.
```python
self.NameModule = "/MyModule"
```

**Note:** This name must be unique and cannot coincide with the name of any other module, and it must be identical to the key of the configuration file.
#### 📌 requirements

```python
def requirements(self):
    requeriments = {
        'CommandExecution': "/mymodule_name",
        'ExternalModules': [
            'commandsFile', 'Communicate'
        ]
    }
    return requeriments
```
This function is in charge of defining the module requirements, in this case it is defined that the execution command is `/mymodule_name` and that the `commandsFile` and `Communicate` modules are needed.
There are other external modules that can be used, these are:

- `commandsFile` - **(Obligatory)** Allows access to the list of module execution commands.
- `Communicate` - Allows you to write and send messages using the whatsapp chat.
- `InterfaceController:` - It allows to obtain the browser instance to be able to interact with the browser interface and use it outside of whatsapp.
- `Schedule:` - Allows you to schedule tasks to run at specific times.

#### 📌 set_commands
The following functions must exist in the module depending on the requirements that are defined in the `requirements` function:

```python
    def set_Communicate(self, Communicate):

    def set_commandFile(self, commandsFile):

    def set_InterfaceController(self, InterfaceControl):

    def set_Schedule(self, Schedule):
```

These functions are in charge of receiving the instances of the external modules that are defined in the `requirements` function and storing them in variables to be able to use them in the module.

## 🏃🏽‍♂️ Running the module

Start the bot, it will take care of loading the module automatically.

Si ocurre algun problema con el módulo dirígete a la carpeta `Logs` y revisa el archivo `Log.txt` para ver los posibles errores.
```bash
SRC/Data/Log/Log.txt
```

#### 💬 Calling the module

Go to your WhatsApp application and write the command to execute the module, for example: `/mymodule_name`
