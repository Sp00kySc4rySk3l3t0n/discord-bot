import discord
from discord import Embed
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import os
import yt_dlp as youtube_dl
from dotenv import load_dotenv

# Configura los intents necesarios para la funcionalidad del bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True
intents.message_content = True
last_known_patch = None

# URL base para la verificación de nuevos parches de League of Legends
BASE_URL = "https://www.leagueoflegends.com/es-es/news/game-updates/"

# Variable para mantener el último parche conocido
last_known_patch = None

# Carga variables de entorno desde el archivo .env
load_dotenv()

# Definición de la clase YTDLSource para manejar la descarga y reproducción de audio
class YTDLSource(discord.PCMVolumeTransformer):
    # Constructor de la clase
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

     # Método de clase para obtener una fuente de audio desde una URL de YouTube
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        ytdl_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'extract_flat': True
        }

        # Ruta al ejecutable de ffmpeg
        ffmpeg_executable_path = "C:\\ffmpeg-7.0\\bin\\ffmpeg.exe"  # Ajusta esta ruta según necesites

        # Crea una instancia de yt_dlp con las opciones y extrae la información
        ytdl = youtube_dl.YoutubeDL(ytdl_options)
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if 'entries' in data:
            data = data['entries'][0]

        url = data['url']
        return cls(discord.FFmpegPCMAudio(url, executable=ffmpeg_executable_path), data=data)  # Pasar correctamente el executable

# Inicialización del bot con el prefijo y los intents
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Carga el ID del servidor y el canal desde las variables de entorno
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Función para leer el último parche conocido desde un archivo de texto
def read_last_known_patch():
    try:
        with open('last_known_patch.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Función para guardar el último parche conocido en un archivo de texto
def save_last_known_patch(patch_url):
    with open('last_known_patch.txt', 'w') as file:
        file.write(patch_url)

# Lee el último parche conocido al iniciar el bot
last_known_patch = read_last_known_patch()

# Evento que se dispara cuando el bot está listo para ser usado
@bot.event
async def on_ready():
    global last_known_patch
    last_known_patch = read_last_known_patch()  # Lee el último parche conocido cuando el bot se inicia
    print(f'Logged in as {bot.user.name}')
    check_for_new_patch.start()


# Comandos slash para interactuar con el bot
@bot.slash_command(guild_ids=[GUILD_ID], description="Saluda al usuario.")
async def greet(ctx):
    embed = Embed(title="Saludo", description="Hola, soy el nuevo bot de discord", color=0x00ff00)
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="Únete al canal de voz del usuario.")
async def join(ctx):
    await ctx.defer()
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        embed = Embed(title="Conexión de Voz", description=f"Conectado al canal: {channel.name}", color=0x00ff00)
        await ctx.followup.send(embed=embed)
    else:
        embed = Embed(title="Conexión de Voz", description="No estás en un canal de voz.", color=0xff0000)
        await ctx.followup.send(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="Reproduce una canción de YouTube.")
async def play(ctx, *, url: str):
    await ctx.defer()
    player = await YTDLSource.from_url(url, loop=ctx.bot.loop)
    if ctx.voice_client is not None:
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        embed = Embed(title="Ahora reproduciendo", description=f"[{player.title}]({url})", color=0x00ff00)
        await ctx.followup.send(embed=embed)
    else:
        embed = Embed(title="Reproducción de Música", description="No estoy en un canal de voz.", color=0xff0000)
        await ctx.followup.send(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="Detiene la reproducción de la música.")
async def stop(ctx):
    await ctx.defer()
    if ctx.voice_client:
        ctx.voice_client.stop()
        embed = Embed(title="Reproducción de Música", description="Reproducción detenida.", color=0x00ff00)
        await ctx.followup.send(embed=embed)
    else:
        embed = Embed(title="Reproducción de Música", description="No estoy conectado a un canal de voz.", color=0xff0000)
        await ctx.followup.send(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="Desconecta al bot del canal de voz.")
async def desconectar(ctx):
    await ctx.defer()
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        embed = Embed(title="Desconexión de Voz", description="He sido desconectado del canal de voz.", color=0x00ff00)
        await ctx.followup.send(embed=embed)
    else:
        embed = Embed(title="Desconexión de Voz", description="No estoy conectado a ningún canal de voz.", color=0xff0000)
        await ctx.followup.send(embed=embed)

# Tarea programada para comprobar la existencia de nuevos parches de League of Legends
@tasks.loop(hours=24)
async def check_for_new_patch():
    global last_known_patch
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('a', class_='style__Wrapper-sc-1h41bzo-0')
        if article:
            current_patch_url = "https://www.leagueoflegends.com" + article.get('href')
            if current_patch_url != last_known_patch:
                last_known_patch = current_patch_url
                save_last_known_patch(last_known_patch)  # Guarda el nuevo parche en el archivo
                channel = bot.get_channel(CHANNEL_ID)  # Asegúrate de que este es el ID correcto del canal
                if channel:
                    await channel.send(f"🆕 Nueva actualización de League of Legends disponible: {current_patch_url}")
            else:
                print("No new patch found.")
        else:
            print("No articles found.")
    else:
        print("Failed to reach the League of Legends updates page.")

# Inicio del bot con el token obtenido de las variables de entorno
bot.run(os.getenv('TOKEN'))
