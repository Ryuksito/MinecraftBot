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
    try:
        await ctx.respond("Apagando el servidor...")
        subprocess.run(['sudo', 'shutdown', 'now'])
    except Exception as e:
        await ctx.respond(f"Error: {str(e)}")

@bot.slash_command(name="reboot", description="Reinicia el servidor (requiere permisos sudo).")
async def reboot(ctx: discord.ApplicationContext):
    try:
        await ctx.respond("Reiniciando el servidor...")
        subprocess.run(['sudo', 'reboot', 'now'])
    except Exception as e:
        await ctx.respond(f"Error: {str(e)}")



@bot.slash_command(name="start-minecraft", description="Inicia el servidor de Minecraft")
async def start_minecraft(ctx: discord.ApplicationContext):
    role_id = 1287285939751747666 
    role = ctx.guild.get_role(role_id)

    await ctx.respond(f"{role.mention} Iniciando el servidor de Minecraft...")

    try:
        # Cambia al directorio y ejecuta el script run.sh con sudo desde allí
        process = subprocess.Popen(
            ['sudo', './run.sh'], 
            cwd='/home/minecraft/minecraft-server',  # Establece el directorio de trabajo
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )

        await ctx.send("Servidor de Minecraft iniciado. Espera unos 2 min...")
        
    except Exception as e:
        print(e)
        await ctx.send(f"Error al ejecutar el comando: {str(e)}")

bot.run(os.getenv('TOKEN'))
