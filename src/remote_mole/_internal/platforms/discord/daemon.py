import configparser
import logging
import sys

from discord.ext import commands

from remote_mole.setup.entrypoint import CONFIG_PATH
from remote_mole._internal.services.ngrok import (
    authenticate,
    set_region,
    Tunnel,
    TunnelAlredyOpenError,
)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger('remote_mole')

config = configparser.ConfigParser()
config.optionxform = str
config.read(CONFIG_PATH)

description = 'A mole that digs tunnels for you.'

# FIXME: the configparser deletes the blank space at the end of the keyword
bot = commands.Bot(
    command_prefix=config['Discord']['keyword'] + ' ',
    description=description
)

SUPPORTED_TUNNELS = (
    'ssh',
    'jupyter',
)


def _format_string_as_code(string):
    return f'`{string}`'


def _format_string_as_codeblock(string, language=''):
    return f'```{language}\n{string}\n```'


@bot.event
async def on_ready():
    log.info(f'Logged in as {bot.user.name}, {bot.user.id}')
    keyword = config['Discord']['keyword']
    log.info(f'Listening to {keyword}')
    authenticate(config['ngrok']['ngrok_token'])
    log.info('Ngrok auth complete.')
    region = config['ngrok']['region']
    set_region(region)
    log.info(f'Ngrok region set to {region}.')
    bot.tunnels = {}


def get_connection_instructions(tunnel, tunnel_type):
    if tunnel_type == 'ssh':
        return _format_string_as_code(
            f'ssh tu_usuario@{tunnel.address} -p {tunnel.port}'
        )
    elif tunnel_type == 'jupyter':
        return _format_string_as_code(
            f'On the browser -> http://{tunnel.address}'
        )


@bot.command()
async def tunnel(ctx, tunnel_type):
    """Digs a tunnel via ngrok, depending on tunnel_type

    Usage:
    tunnel tunnel_type

    Creates a tunnel, and if such tunnel is already created just
    passes said open tunnel.

    To know which tunnel types are supported use get_tunnel_types
    command.
    """
    if tunnel_type not in SUPPORTED_TUNNELS:
        await ctx.send(
            f"Hey... I don't know about {tunnel_type} tunnels :grimacing:"
        )
        raise ValueError('User wanted to create unknown tunnel.')

    try:
        tunnel = Tunnel(tunnel_type)
    except TunnelAlredyOpenError:
        instructions = get_connection_instructions(
            bot.tunnels[tunnel_type], tunnel_type
        )
        await ctx.send(
            f'A {tunnel_type} tunnel was already created. \n {instructions}'
        )
    else:
        log.info('Tunnel created successufully')
        instructions = get_connection_instructions(tunnel, tunnel_type)
        bot.tunnels[tunnel_type] = tunnel
        await ctx.send(
            f'Tunnel created, to connect: \n {instructions}'
        )
        if tunnel_type == 'jupyter':
            await ctx.send(
                'psst, you! I hope the notebook is password protected! \n' +
                'call me with `jupyter_advice` command if you need a hand.'
            )


@bot.command()
async def close_tunnel(ctx, tunnel_type):
    """Closes ngrok tunnel

    Usage:
    close_tunnel tunnel_type
    """
    if tunnel_type not in SUPPORTED_TUNNELS:
        await ctx.send(
            f"Hey... I don't know about {tunnel_type} tunnels :grimacing:"
        )
        raise ValueError('User wanted to create unknown tunnel.')

    if tunnel_type not in bot.tunnels.keys():
        await ctx.send(
            f"I don't remember creating a {tunnel_type} tunnel :thinking:"
        )
    else:
        log.info(f'About to close {tunnel_type} tunnel')
        bot.tunnels[tunnel_type].close()
        await ctx.send(
            f'There... {tunnel_type} tunnel closed.'
        )


@bot.command()
async def get_tunnel_types(ctx):
    """Gives info about tunnel types"""
    await ctx.send(
        f"Right now supported tunnels are {SUPPORTED_TUNNELS}"
    )


@bot.command()
async def jupyter_advice(ctx):
    """Gives advice on sharing jupyter notebooks"""
    gen_config_cmd = _format_string_as_codeblock(
        'jupyter notebook --generate-config',
        'bash',
    )
    allow_remote_cmd = _format_string_as_codeblock(
        "echo \"c.NotebookApp.allow_remote_access = True\" " +
        ">> ~/.jupyter/jupyter_notebook_config.py",
        'bash',
    )
    notebook_pass_cmd = _format_string_as_codeblock(
        'jupyter notebook password',
        'bash',
    )
    await ctx.send(
        "First of all, you need to have jupyter installed in the target. " +
        "that's quite easy, so i'll leave the research for you. \n \n" +
        "The other thing you'll need to worry about is allowing remote" +
        "access to the notebooks, run the following commands: \n" +
        gen_config_cmd + "\n" + allow_remote_cmd + "\n \n" +
        "Last but not least, put a password to your notebook:\n" +
        notebook_pass_cmd + "\n" +
        "otherwise you will go straight to cibersecurity hell."
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        help_cmd = _format_string_as_code("che topo: help")
        await ctx.send(
            "Hey! I don't understand :thinking: \n" +
            f"maybe try with {help_cmd}"
        )


bot.run(config['Discord']['token'])
