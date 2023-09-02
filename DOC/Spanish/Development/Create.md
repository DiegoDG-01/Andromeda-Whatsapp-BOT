## Importante 
#### Estamos actualizando nuestros documentos de desarrollo hacia una nueva versión, por lo que recomendamos que no se siga este documento hasta que se termine de actualizar. Lamentamos las molestias.

## Desarrollar módulos para Andromeda - Whatsapp BOT

En este documento se explica como desarrollar un módulo para Andromeda siguiendo los estandares requeridos por el proyecto.

## 💡 Entendiendo el desarrollo de un módulo

Un módulo consta de tres archivos principales:
- El archivo python que contiene la lógica.
- El archivo con los mensajes que se enviarán al usuario (errores, éxitos, información, etc).
- El archivo con la configuración del módulo (Nombre, descripción, args o funciones disponibles).

## 💬 Creando el archivo de mensajes

Este archivo **no es obligatorio**, pero es recomendable para tener un control de los mensajes que se enviarán al usuario, además si se plantea que su módulo trabaje en varios idiomas, este archivo será el encargado de almacenar los mensajes en cada idioma.
<br>

Esta decisión es del desarrollador, pero se recomienda que se cree este archivo.

Deberás crear un archivo **json** con el nombre de tu módulo `MyModule.json` en la siguiente ruta 
```bash
SRC/Data/Modules/Messages/MyModule.json
``` 
y dentro de este archivo deberás colocar los mensajes que se enviarán al usuario, por ejemplo:
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
Estos mensajes serán controlados completamente por su módulo, con lo cual no esta obligado a usar una estructura como la anterior, pero si es recomendable para mantener un orden en los mensajes.

**Nota**: Podras acceder al legunaje que se esta usando en el bot desde la variable de entorno `Language` que se encuentra en el archivo `.env`.

```python
from os import environ

lang = environ.get('Language')
```

## ⚙️ Creando el archivo de configuración

Se debera crear un archivo **json** con el nombre de tu módulo `MyModule.json` en la siguiente ruta 
```bash
SRC/Data/Modules/Codes/MyModule.json
```

Este archivo es el encargado de almacenar la configuración del módulo, el nombre necesario para ser llamado, descripción, argumentos o funciones, etc.

Este archivo deberá tener la siguiente estructura:
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

**Importante:** El nombre del módulo debe ser el mismo que el nombre del archivo python que contiene la lógica del módulo.

- **English**: Es el idioma en el que se encuentra la configuración del módulo, en este caso es el inglés.
- **/MyModule**: Es el nombre del módulo, este nombre será el que se usará para localizar el módulo de manera interna.
- **Desc**: Es la descripción del módulo, esta descripción será mostrada al usuario cuando ejecute el comando `/mymodule_name` or `/mymodule_name -d`.
- **Args**: Es la lista de argumentos que tendrá el módulo, estos argumentos serán los que se usarán para ejecutar las funciones del módulo, por ejemplo: `/mymodule_name -arg`, puede contener **n** argumentos dependiendo de las funciones que realizara el bot.


- Los siguientes argumentos son obligatorios:
- **-d**: Es el argumento que se usará para listar los argumentos disponibles del módulo, este argumento es obligatorio para que el módulo pueda ser ejecutado.
- **-l**: Es el argumento que se usará para listar los argumentos disponibles del módulo, este argumento es obligatorio para que el módulo pueda ser ejecutado.

**Nota:** es obligatorio que el archivo de configuración siga el mismo patrón que el ejemplo anterior.

**Nota #2:** Se elimino la necesidad de tener un objeto `Lang` en el archivo de configuración, ahora el idioma por defecto que tomara el módulo será el idioma que se encuentre en la configuración del bot en su archivo .env en la raíz del proyecto.
Establezca los idiomas como llaves en el archivo de configuración, si el idioma es completamente diferente al idioma por defecto del bot establezca la llave como **Default** así no importara el idioma que se establezca en la configuración del bot.

```json
{
  "Default": {
    . . .
  }
}
```

## 🐍 Creando el archivo de python

En la siguiente ruta encontrarás un archivo llamado `Base.py` este archivo contiene las funciones básicas que debe tener un módulo para que funcione correctamente.
Asi que deberas importar este archivo en tu módulo para que pueda funcionar correctamente.

```bash
SRC/Functions/Base.py
```

### 📝 Funciones básicas

Esta es una breve explicación de las funciones que contiene el archivo `Base.py` y que son implementadas para el correcto funcionamiento.

#### 📌 __init__

En este apartado se establece el nombre del módulo en la variable `self.NameModule`.

```python
self.NameModule = f"/{self.NameModule}"
```

**Nota:**  Este nombre tiene que ser único y no puede coincidir con el nombre de ningún otro módulo, además que tiene que ser idéntico a la llave del archivo de configuración.

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
Esta función es la encargada de definir los requerimientos del módulo, en este caso se define que el comando de ejecución desde WhatsApp sea el mismo que el nombre del módulo y los modulos que se necesitan son `commandsFile` y `Communicate`.
además existen otros modulos externos que se pueden utilizar, estos son:

- `commandsFile` - **(Obligarotio)** Permite acceder a la lista de los comandos de ejecución de los módulos.
- `Communicate` - **(Obligarotio)** Permite escribir y enviar mensajes usando el chat de whatsapp.
- `InterfaceController:` - Permite obtener la instancia del navegador para poder interactuar con la interfaz del navegador y hacer uso del mismo fuera de whatsapp.
- `Schedule:` - Permite programar tareas para que se ejecuten en momentos determinados.

Las dependencias es un diccionario que contiene los módulos externos que se necesitan para que el módulo funcione correctamente, en este caso se necesita el módulo `Whisper` en su versión `0.2.0`, de no ser tener ninguna dependencia se puede omitir este apartado.

**Importante:** Esta función puede ser sobreescrita desde el archivo del módulo para agregar más módulos o dependencias.


#### 📌 set_commands

```python
    def set_Communicate(self, Communicate):

    def set_commandFile(self, commandsFile):

    def set_InterfaceController(self, InterfaceControl):

    def set_Schedule(self, Schedule):
```

Estas funciones son las encargadas de recibir las instancias de los módulos externos que se definan en la función `requirements` y almacenarlas en variables para poder usarlas en el módulo.

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

Esta función es la encargada de gestionar los comandos que se ejecutan desde WhatsApp, en este caso se definen dos comandos que son `-d` y `-l`, estos comandos son funciones obligatorias para que el módulo pueda ser ejecutado con las funciones básicas.

Puede ser sobreescrita desde el archivo del módulo para agregar más comandos pero manteniendo los comandos `-d` y `-l` para que el módulo pueda ser ejecutado.

### 🧑🏻‍💻 Creando nuestro módulo

Ahora que ya entendemos como funciona el archivo `Base.py` podemos crear nuestro módulo.    

Para crearlo deberemos generar un archivo con el nombre de nuestro módulo `MyModule.py` en la siguiente ruta:
```bash 
SRC/Modules/MyModule.py
```

Ahora deberemos importar el archivo `Base.py`, crear una clase para nuestro módulo y heredar la clase `BaseModule` y pasarle el nombre de nuestro módulo como parámetro a la clase padre.
```python
from Functions.Base import BaseModule

class MyModule(BaseModule):

    def __init__(self):
        # Inicializamos la clase padre y le pasamos el de nuestro módulo
        super().__init__("MyModule")
```

Si nuestro módulo necesita de otros módulos externos deberemos sobreescribir la función `requirements` y agregar los módulos que necesitamos, por ejemplo:
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

Tambien deberemos sobreescribir la función `CommandManager` para agregar los comandos que necesitamos, por ejemplo:

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

De aquí en adelante ya puedes crear las funciones que necesites para tu módulo, por ejemplo:

```python
    def MyNewFunction(self):
        self.Communicate.WriteMessage("Hello World")
        self.Communicate.SendMessage()
        return True
```

Asegurate de que la función se encuentre tanto en el archivo de `configuraciones` como dentro de la función `CommandManager` para que pueda ser ejecutada.

## 🏃🏽‍♂️ Ejecutando el módulo

Inicia el bot, él se encargará de cargar el módulo automáticamente.

Si ocurre algun problema con el módulo dirígete a la carpeta `Logs` y revisa el archivo `Log.txt` para ver los posibles errores.
```bash
SRC/Data/Log/Log.txt
```

#### 💬 Llamando al módulo

Dirígete a tu aplicación de WhatsApp y escribe el comando de ejecución del módulo, por ejemplo: `/mymodule_name`

