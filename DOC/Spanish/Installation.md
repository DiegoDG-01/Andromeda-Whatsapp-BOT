## Instalar Andromeda - WhatsApp Bot

### 📋 Tabla de contenidos

* [Requerimientos](#requirements)
* [Navegadores compatibles](#browsers)
* [Instalación](#installation)
    * [Ejecutables](#ExecutableInstallation)
    * [Instalación manual](#ManualInstallation)
    * Docker (descontinuado)
    * Instalador (descontinuado)
    * Instalador windows (descontinuado)
* [Iniciar el bot](#init)
    * [Ejecutables](#ExeInit)
    * [Instalación manual](#ManualInit)


## <a name="requirements"></a> 📝 Requerimientos

Compatibilidad con sistemas operativos:

- Linux
- Mac OS
- Windows 10/11

Necesitas tener instalado los siguientes programas:

- Git
- Python 3.8 o superior
- Google Chrome o Microsoft Edge

## <a name="browsers"></a> 🌐 Navegadores compatibles

Actualmente, el bot es compatible con los siguientes navegadores:

 - Google Chrome 98 o posterior
 - Microsoft Edge 115 o posterior

La compatibilidad con Firefox es experimental, se encontraron algunos problemas que se están solucionando, en proximas versiones se agregará soporte.

## <a name="installation"></a> 💻 Instalación


### <a name="ExecutableInstallation"></a> 📦 Ejecutables (Beta)

Seguimos trabajando en simplificar el uso de andromeda, por lo que hemos creado ejecutables para los distintos tipos de sistemas operativos, estos ejecutables son versiones beta, por lo que pueden contener errores o no trabajar correctamente.


1. Para descargar los ejecutables, dirígete a la sección [GitHub Release](https://github.com/DiegoDG-01/Whatsapp_BOT/releases) (Apartir de la versión 0.4.0 están disponibles los ejecutables)


2. Descarga y descomprime el ejecutable para tu sistema operativo.


3. Accede a la carpeta **"SRC/Data/Config/Lang"** esta carpeta contiene los archivos de lenguajes (actualmente solo en español e inglés), copia el archivo **Codes.json** y **Config.json** del lenguaje que quieres usar y pegalo en la carpeta **"SRC/Data/Config"**.
 
     ```
     SRC/Data/Config/Codes.json
     SRC/Data/Config/Config.json
     ```
   
4. Abre el archivo **"SRC/Data/Config/Config.json"** y dirígete a la sección **"Default"** y reemplaza el valor de **"WhatsappName"** con el nombre del chat que deseas usar para que el bot esté esperando los comandos.

    ```
    "Default": {
            "WhatsappName":"MiChat"
            "WhatsappNumber":"",
            "WhatsappGroupName":""


5. Por defecto el navegador a utilizar es **Google Chrome**, si quieres usar Microsoft Edge u otro navegador, dirígete a la raiz del proyecto y abre el archivo **.env** y reemplaza el valor de **"DefaultBrowser"** con el nombre del navegador que quieres usar (**chrome** o **edge**).


6. En el mismo archivo .env asegúrate de establecer el idioma de acuerdo al lenguaje que seleccionaste en el apartado 3 (**Spanish** o **English**).
      

### <a name="ManualInstallation"></a> 👋🏼 Instalación manual

Para instalar el bot manualmente, siga los siguientes pasos:

1. Descarga la última versión del bot desde [GitHub Release](https://github.com/DiegoDG-01/Whatsapp_BOT/releases) o usando **Git** en tu terminal:
    ```
    git clone "https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT.git"
    ```

2. Copia el folder descargado al directorio que mejor te convenga.


3. Accede a la carpeta del proyecto desde la terminal:
    ```
    cd Ruta-Elegida/Andromeda-Whatsapp_BOT
    ```


4. (**Opcional**) Instala el paquete para generar entornos virtuales de Python
    ```
    pip3 install virtualenv
    ```
   
5. (**Opcional**) Crea el entorno virtual
    ```
    virtualenv -p python3 .venv
    ```
   
6. (**Optional**) Activa el entorno virtual

    **Unix/Linux:**
    ```
    source .venv/bin/activate
    ```
   
    **Windows:**
    ```
    .venv\\Scripts\\activate.bat
    ```

7. Una vez dentro en la carpeta del bot ejecuté el siguiente comando para instalar las dependencias:
    ```
    python3 pip install -r requirements.txt
    ```



8. (**Opcional Unix/Linux**) Ejecuté el siguiente comando si quiere crear un alias para ejecutar el bot de manera más fácil desde la terminal.
    
    **Si usas bash:**
    ```
    echo 'alias andromeda="cd /Ruta-Elegida/Andromeda-Whatsapp_BOT/SRC/ && source .venv/bin/activate && python3 entrypoint.py"' >> ~/.bashrc
    ```
    
    **Si usas zsh:**
    ```
    echo 'alias andromeda="cd /Ruta-Elegida/Andromeda-Whatsapp_BOT/SRC/ && source .venv/bin/activate && python3 entrypoint.py"' >> ~/.zshrc
    ```
   
   Reemplaza **"Ruta-Elegida"** por la ruta donde se encuentra el folder del proyecto.

   
9. (**Obligatorio**) Accede a la carpeta **"SRC/Data/Config/Lang"** esta carpeta contiene los archivos de lenguajes (actualmente solo en español e inglés), copia el archivo **Codes.json** y **Config.json** del lenguaje que quieres usar y pegalo en la carpeta **"SRC/Data/Config"**.
 
     ```
     SRC/Data/Config/Codes.json
     SRC/Data/Config/Config.json
     ```
   
10. (**Obligatorio**) Abre el archivo **"SRC/Data/Config/Config.json"** y dirígete a la sección **"Default"** y reemplaza el valor de **"WhatsappName"** con el nombre del chat que deseas usar para que el bot esté esperando los comandos.

    ```
    "Default": {
            "WhatsappName":"MiChat"
            "WhatsappNumber":"",
            "WhatsappGroupName":""
        }
    ```
    
11. Dirígete a la sección [Iniciar Bot](#init).


## 😎 Iniciar el bot <a name = "init"></a>

* [Ejecutables](#ExeInit)
* [Instalación manual](#ManualInit)


### <a name="ExeInit"></a> ⚙️ Ejecutables (Beta)

Si descargaste el ejecutable para tu sistema operativo, solo debes iniciar el archivo **"Andromeda"**
y escanear el código QR con tu teléfono y esperar a que el bot inicie sesión.

Windows y Linux:

<img src="../IMG/UI-Whatsapp_Init_Page.png" width="30%">

Mac OS:

<img src="../IMG/Whatsapp_Init_Page.png" width="30%">

**Nota:** Si usas Mac OS, el codigo QR se mostrará en la terminal ya que existe un problema que se está solucionando, en proximas versiones se agregará soporte.

### <a name=""></a> 📝 Iniciar el bot manualmente


1. Desde la terminal, accede a la carpeta **"SRC"** del proyecto:

    **Unix/Linux:**
    ```
    cd Ruta-Elegida/Andromeda-Whatsapp_BOT/SRC/
    ```
    
    **Windows:**
    ```
    cd Ruta-Elegida\Andromeda-Whatsapp_BOT\SRC\
    ```

   Reemplaza **"Ruta-Elegida"** por la ruta donde se encuentra el folder del proyecto.


2. Ejecuta el siguiente comando para iniciar el bot:
    
   ```
    python3 entrypoint.py
    ```
   
3. Escanea el código QR con tu teléfono y espera a que el bot inicie sesión.

    Windows y Linux:

   <img src="../IMG/UI-Whatsapp_Init_Page.png" width="30%">
   
   Mac OS:
   
   <img src="../IMG/Whatsapp_Init_Page.png" width="30%">
   
   **Nota:** Si usas Mac OS, el codigo QR se mostrará en la terminal ya que existe un problema que se está solucionando, en proximas versiones se agregará soporte.