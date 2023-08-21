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

## ⚙️ Creando el archivo de configuración

Se debera crear un archivo **json** con el nombre de tu módulo `MyModule.json` en la siguiente ruta 
```bash
SRC/Data/Modules/Codes/MyModule.json
```

Este archivo es el encargado de almacenar la configuración del módulo, como el nombre para su ejecución, descripción, argumentos o funciones, etc.

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

~~- **Lang**: Es el idioma por defecto del módulo, en este caso es el inglés.~~
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

En la siguiente ruta encontrarás un archivo llamado `Example.py` que contiene la plantilla con las funciones básicas necesarias para desarrollar un módulo.

```bash
SRC/Functions/Example.py
```

Copia el archivo en la misma ruta y renómbralo con el nombre que quieras para tu módulo, por ejemplo `MyModule.py` 

```bash
SRC/Functions/MyModule.py
```

### 📝 Funciones básicas

En el archivo `MyModule.py` encontrarás las siguientes funciones:

#### 📌 __init__

En este apartado deberás establecer el nombre del módulo en la variable `self.NameModule` incluido el `/` al inicio.

```python
self.NameModule = "/MyModule"
```

**Nota:**  Este nombre tiene que ser único y no puede coincidir con el nombre de ningún otro módulo, además que tiene que ser idéntico a la llave del archivo de configuración.

#### 📌 requirements

```python
def requirements(self):
    requeriments = {
        'CommandExecution': "/mymodule_name",
        'ExternalModules': [
            'commandsFile', 'Communicate'
        ],
        'Dependencies': {
            'Whisper':'0.2.0'
        }
    }
    return requeriments
```
Esta función es la encargada de definir los requerimientos del módulo, en este caso se define que el comando de ejecución desde WhatsApp sea `/mymodule_name` y que se necesitan los módulos `commandsFile` y `Communicate`.
además existen otros modulos externos que se pueden utilizar, estos son:

- `commandsFile` - **(Obligarotio)** Permite acceder a la lista de los comandos de ejecución de los módulos.
- `Communicate` - Permite escribir y enviar mensajes usando el chat de whatsapp.
- `InterfaceController:` - Permite obtener la instancia del navegador para poder interactuar con la interfaz del navegador y hacer uso del mismo fuera de whatsapp.
- `Schedule:` - Permite programar tareas para que se ejecuten en momentos determinados.

Las dependencias es un diccionario que contiene los módulos externos que se necesitan para que el módulo funcione correctamente, en este caso se necesita el módulo `Whisper` en su versión `0.2.0`.

Dependiendo de los módulos externos que se necesiten, se deberá agregar al diccionario.


#### 📌 set_commands
Las siguientes funciones deberán existir en el módulo dependiendo los requerimientos que se definan en la función `requirements`:

```python
    def set_Communicate(self, Communicate):

    def set_commandFile(self, commandsFile):

    def set_InterfaceController(self, InterfaceControl):

    def set_Schedule(self, Schedule):
```

Estas funciones son las encargadas de recibir las instancias de los módulos externos que se definan en la función `requirements` y almacenarlas en variables para poder usarlas en el módulo.

## 🏃🏽‍♂️ Ejecutando el módulo

Inicia el bot, él se encargará de cargar el módulo automáticamente.

Si ocurre algun problema con el módulo dirígete a la carpeta `Logs` y revisa el archivo `Log.txt` para ver los posibles errores.
```bash
SRC/Data/Log/Log.txt
```

#### 💬 Llamando al módulo

Dirígete a tu aplicación de WhatsApp y escribe el comando de ejecución del módulo, por ejemplo: `/mymodule_name`

