import discord
import asyncio
import git
import message
import glob
import time
from pluginbase import PluginBase

startTime = time.time()

plugin_base = PluginBase(package='plugins')
plugin_source = plugin_base.make_plugin_source(searchpath=['./plugins'])

plugins = []
commands = []

for plugin in plugin_source.list_plugins():
    plugin_temp = plugin_source.load_plugin(plugin)
    plugin_info = plugin_temp.onInit(plugin_temp)
    if plugin_info.plugin == None:
        print("Plugin not defined!")
        pass
    if plugin_info.name == None:
        print("Plugin name not defined")
        pass
    if plugin_info.commands == []:
        print("Plugin did not define any commands.")
        pass
    plugins.append(plugin_info)
    for command in plugin_info.commands:
        if command.plugin == None:
            print("Plugin command does not define parent plugin")
            pass
        if command.name == None:
            print("Plugin command does not define name")
            pass
        commands.append(command)
        print("Command `{}` registered successfully.".format(command.name))
    print("Plugin '{}' registered successfully.".format(plugin_info.name))

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence(game=discord.Game(name='!help - Pooter 2.0'))

@client.event
async def on_message(message_in):

    if message_in.server == None:
        return
    
    if message_in.author.id == client.user.id:
        return

    if message_in.content.startswith('!cachecontents'):
        cacheCount = glob.glob('cache/{}_*'.format(message_in.content.split(' ')[-1]))
        cacheString = '\n'.join(cacheCount)
        await client.send_message(message_in.channel, '```{}```'.format(cacheString))
    for command in commands:
        if message_in.content.split(' ')[0] == '!' + command.name or message_in.content == '!' + command.name:
            await client.send_typing(message_in.channel)
            message_recv = message.message
            message_recv.command = command.name
            message_recv.body = message_in.content.split('!' + command.name)[1]
            message_recv.author = message_in.author
            message_recv.server = message_in.server

            command_result = command.plugin.onCommand(message_recv)

            # No message, error.
            if command_result == None:
                await client.send_message(message_in.channel, '**Beep boop - Something went wrong!**\n_Command did not return a result._')
            
            # Do list of messages, one after the other.
            elif type(command_result) is list:
                for item in command_result:
                    await process_message(message_in, item)

            # Do regular message.
            else:
                await process_message(message_in, command_result)

                # Do we delete the message afterwards?
                if command_result.delete:
                    await client.delete_message(message_in)

async def process_message(message_in, msg):
    if msg.body != '' or msg.embed != None:
        if msg.embed != None:
            if msg.body == '':
                await client.send_message(message_in.channel, embed=msg.embed)
            else:
                zerospace = "​"
                msg.body = msg.body.replace("@everyone", "@{}everyone".format(zerospace)).replace("@here", "@{}here".format(zerospace))
                await client.send_message(message_in.channel, msg.body, embed=msg.embed)
        else:
            zerospace = "​"
            msg.body = msg.body.replace("@everyone", "@{}everyone".format(zerospace)).replace("@here", "@{}here".format(zerospace))
            await client.send_message(message_in.channel, msg.body)
    if msg.file != '':
        await client.send_file(message_in.channel, msg.file)

token = ''
with open('token.txt') as m:
    token = m.read().strip()

client.run(token)
