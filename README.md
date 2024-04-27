# Bot de Discord

Este es un bot de Discord que realiza varias funciones, como unirse a canales de voz, reproducir música de YouTube y comprobar actualizaciones de League of Legends.

## 🛠 Instalación

Para instalar las dependencias necesarias para este proyecto, debes tener Python y pip ya instalados en tu sistema. Luego, ejecuta el siguiente comando en la raíz del proyecto:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración
### Variables de Entorno
Antes de ejecutar el bot, necesitas configurar algunas variables de entorno que el bot usará para su funcionamiento. Debes crear un archivo .env en la raíz del proyecto con las siguientes variables:

```bash
DISCORD_TOKEN=TuTokenDeDiscord
GUILD_ID=IDDeTuServidor
CHANNEL_ID=IDDelCanal
```

Reemplaza TuTokenDeDiscord, IDDeTuServidor, e IDDelCanal con tus propios valores reales:

 - DISCORD_TOKEN: El token de tu bot de Discord.
 - GUILD_ID: El ID del servidor de Discord donde tu bot estará activo.
 - CHANNEL_ID: El ID del canal de Discord donde el bot enviará mensajes y actualizaciones.

## 🚀 Ejecución
Para ejecutar el bot, usa el siguiente comando desde la línea de comandos en la raíz de tu proyecto:

```bash
python main.py
```

Este comando iniciará el bot, y debería estar listo para responder a comandos en Discord.