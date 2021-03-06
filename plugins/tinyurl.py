import plugin
import command
import message
from urllib.request import urlopen

def onInit(plugin):
    tinyurl_command = command.command(plugin, 'tinyurl', shortdesc='Convert a link to a TinyURL')
    return plugin.plugin.plugin(plugin, 'tinyurl', [tinyurl_command])

def onCommand(message_in):
    return message.message(body=urlopen("http://tinyurl.com/api-create.php?url=" + message_in.body.strip()).read().decode("utf-8"))