import discord
import os
import subprocess
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="get-ip", description="get ip from the server")
async def get_ip(ctx: discord.ApplicationContext):
    ip = os.popen('curl ifconfig.me').read().strip()  # Ejecuta curl y obtiene la IP
    await ctx.respond(f"The server's public IP is: {ip}")

# Comando para apagar el sistema
@bot.slash_command(name="shutdown", description="Apaga el servidor (requiere permisos sudo).")
async def shutdown(ctx: discord.ApplicationContext):
    if str(ctx.author.id) == os.getenv('ADMIN_USER_ID'):
        try:
            await ctx.respond("Apagando el servidor...")
            subprocess.run(['sudo', 'shutdown', 'now'])
        except Exception as e:
            await ctx.respond(f"Error: {str(e)}")
    else:
        await ctx.respond("No tienes permiso para ejecutar este comando.")

@bot.slash_command(name="reboot", description="Reinicia el servidor (requiere permisos sudo).")
async def reboot(ctx: discord.ApplicationContext):
    if str(ctx.author.id) == os.getenv('ADMIN_USER_ID'):
        try:
            await ctx.respond("Reiniciando el servidor...")
            subprocess.run(['sudo', 'reboot', 'now'])
        except Exception as e:
            await ctx.respond(f"Error: {str(e)}")
    else:
        await ctx.respond("No tienes permiso para ejecutar este comando.")

@bot.slash_command(name="start-minecraft", description="Inicia el servidor de Minecraft")
async def start_minecraft(ctx: discord.ApplicationContext):
    if str(ctx.author.id) == os.getenv('ADMIN_USER_ID'):  # Verifica si el usuario es el administrador
        try:
            await ctx.respond("Iniciando el servidor de Minecraft...")
            # Cambia al directorio y ejecuta el script run.sh con sudo
            subprocess.run(['sudo', 'bash', '-c', 'cd /home/minecraft/minecraft-server && ./run.sh'], check=True)
            await ctx.respond("Servidor de Minecraft iniciado.")
        except subprocess.CalledProcessError as e:
            await ctx.respond(f"Error al iniciar el servidor: {str(e)}")
    else:
        await ctx.respond("No tienes permiso para ejecutar este comando.")

bot.run(os.getenv('TOKEN'))
