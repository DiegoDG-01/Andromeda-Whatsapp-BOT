## Instalar Andromeda - WhatsApp Bot

Este bot se está probando actualmente en Mac OS, Linux y Windows, pero el instalador solo funciona en Unix o sistemas operativos derivados y para los sistemas operativos Windows se desarrolló un instalador básico alternativo, o se puede instalar manualmente siguiendo las instrucciones.

## 📕 Requerimientos

Actualmente, el bot es compatible con los siguientes sistemas operativos:

- Windows (solo probado en Windows 10)
- Linux (se requiere el administrador de paquetes APT)
- Mac OS Big Sur o posterior (se requiere el administrador de paquetes Brew)

Necesitas tener instalado los siguientes programas:

- Git
- Google Chrome
- Python 3.8 o posterior

## 🌐 Navegadores compatibles

Actualmente, el bot se prueba en los siguientes navegadores:

 - Google Chrome 98.X o posterior

## 💻 Instalación

* [Instalador Linux](#LinuxInstaller)
* [Instalador Windows](#WinInstaller)
* [Docker](#Docker)
* [Instalación manual](#ManualInstallation)

### <a name="LinuxInstaller"></a> Usar el instalador para Unix/Linux

1. Descarga la última versión del bot desde [GitHub Release](https://github.com/DiegoDG-01/Whatsapp_BOT/releases) o usando **Git** en tu terminal:
     ```
    git clone "https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT.git"
    ```
2. En tu terminal abre la carpeta con el bot y ejecuta el siguiente comando:
    ```
    python3 install.py
    ```
    El instalador muestra el progreso e información importante, espere hasta que la instalación finalice.


3. El instalador solicitará el nombre del chat para usarlo para escuchar los mensajes (se recomienda crear previamente un grupo donde te encuentres **solo tú**.


4. El instalador creará una nueva carpeta con el nombre "Andromeda-Whatsapp_BOT" en tu directorio de inicio.


5. Dirígete al apartado [Inicializar el bot](#init) para continuar.

### <a name="WinInstaller"></a> Usar el instalador para Windows

1. Descarga la última versión del bot desde [GitHub Release](https://github.com/DiegoDG-01/Whatsapp_BOT/releases) o usando **Git** en tu terminal:
     ```
    git clone "https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT.git"
    ```
2. En tu terminal abre la carpeta con el bot y ejecuta el siguiente comando:
    ```
    python3 windows_install.py
    ```
    El instalador muestra el progreso e información importante, espere hasta que la instalación finalice.


4. El instalador solicitará el nombre del chat para usarlo para escuchar los mensajes (se recomienda crear previamente un grupo donde te encuentres **solo tú**.


5. Dirígete al apartado [Inicializar el bot](#init) para continuar.

### <a name="Docker"></a> Instalación desde docker (En desarrollo)

1. Asegurate de tener instalado docker en tu sistema operativo.


2. Descarga la última versión del bot desde [GitHub Release]((https://github.com/DiegoDG-01/Whatsapp_BOT/releases)) o usando **Git** en tu terminal:
    ```
    git clone "https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT.git"
    ```

3. En un editor de texto, abre el archivo "Dockerfile"


4. En la línea 9 (**ENV Language English**) asegurate de establecer el lenguage para el bot, actualmente solo se soporta el inglés y el español.


5. En la línea 10 (**ENV Username "ChatName"**) establece el nombre del chat donde quieres que el bot escuche los mensajes.


6. Abre una terminal en la carpeta donde se encuentra el archivo "Dockerfile" y ejecuta el siguiente comando:
    ```
    docker build -t "andromeda" .
    ```
   
7. Una vez finalizada la construcción de la imagen, dirígete al apartado [Inicializar el bot](#init) para continuar.

### <a name="ManualInstallation"></a> Instalación manual

Si no quieres usar el instalador, puedes instalar el bot manualmente siguiendo las siguientes instrucciones:

1. Descarga la última versión del bot desde [GitHub Release]((https://github.com/DiegoDG-01/Whatsapp_BOT/releases)) o usando **Git** en tu terminal:
    ```
    git clone "https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT.git"
    ```

2. Copia el folder del bot al directorio que elijas.


3. Accede a la carpeta del proyecto


4. (**Opcional**) Instala el paquete para generar entornos virtuales de Python
    ```
    pip3 install virtualenv
    ```
   
5. (**Opcional**) Crea el entorno virtual
    ```
    virtualenv -p python3 .venv
    ```
   
6. (**Optional**) Activa el entorno virtual

    Unix/Linux:
    ```
    source .venv/bin/activate
    ```
   
    Windows:
    ```
    .venv\\Scripts\\activate.bat
    ```

7. Una vez dentro en la carpeta del bot ejecuté el siguiente comando para instalar las dependencias:
    ```
    python3 pip install -r requirements.txt
    ```



8. (**Opcional Unix/Linux**) Ejecuté el siguiente comando si quiere crear una alias para ejecutar el bot de manera más fácil
    "Ruta-Elegida" es la ruta donde se encuentra el folder del proyecto y es la ruta del paso 2.
    
    Si usas bash:
    ```
    echo 'alias andromeda="cd /Ruta-Elegida/Andromeda-Whatsapp_BOT/SRC/ && source .venv/bin/activate && python3 entrypoint.py"' >> ~/.bashrc
    ```
    
    Si usas zsh:
    ```
    echo 'alias andromeda="cd /Ruta-Elegida/Andromeda-Whatsapp_BOT/SRC/ && source .venv/bin/activate && python3 entrypoint.py"' >> ~/.zshrc
    ```
   
9. (**Obligatorio**) Accede a la carpeta **"SRC/Data/Config/Lang"** esta carpeta contiene los archivos de lenguajes (actualmente solo en español e inglés), copia el archivo **Codes.json** y **Config.json** pégalo en la carpeta **"SRC/Data/Config"**
 
     ```
     SRC/Data/Config/Codes.json
     SRC/Data/Config/Config.json
     ```
   
10. (**Obligatorio**) Abre el archivo **"SRC/Data/Config/Config.json"** y busca y remplaza el valor de "**WhatsappName**" por el nombre del chat que quieres usar para escuchar los mensajes (se recomienda crear previamente un grupo donde te encuentres **solo tú**).

    ```
    "Default": {
            "WhatsappName":"(CHOSEN_NAME)"
            "WhatsappNumber":"",
            "WhatsappGroupName":""
        }
    ```

## 😎 Iniciar el bot <a name = "init"></a>

Para iniciar el bot ejecuta el siguiente comando:

Si usas el instalador o creaste un alias:
```
ANDROMEDA
```

Si instalaste el bot manualmente y no creaste un alias ("Ruta-Elegida" es la ruta donde se encuentra el folder del proyecto y es la ruta del paso 2):
```
python3 /Ruta-Elegida/Andromeda-Whatsapp_BOT/SRC/entrypoint.py
```

o si está utilizando Docker, la primera vez que ejecuta el bot, debe ejecutar el siguiente comando para iniciar sesión:
```
docker run -it --name andromeda andromeda
```

Si ha iniciado sesión, debe ejecutar el siguiente comando:  
```
docker start andromeda
```

Una vez iniciado el bot, el bot te pedirá que escanees el código QR para iniciar sesión en Whatsapp Web.

<img src="../IMG/Whatsapp_Init_Page.png" width="100%">
