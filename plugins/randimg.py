import urllib.request
import urllib.error
import json
import plugin
import command
import message
import caching
import os

def onInit(plugin):
    star_command = command.command(plugin, 'star', shortdesc='Post a random picture of Star Butterfly to the channel')
    goldfish_command = command.command(plugin, 'goldfish', shortdesc='Post a random picture of a goldfish to the channel')
    return plugin.plugin.plugin(plugin, 'randimg', [star_command, goldfish_command])

def onCommand(message_in):
    # Star
    if message_in.command == 'star':
        try:
            f = urllib.request.urlopen("https://sydneyerickson.me/starapi/rand.php").read().decode("utf-8")
        except urllib.error.URLError as e:
            return message.message(body='There was an issue connecting to Starapi'.format(message_in.body))

        imageName = f.split('/')
        caching.downloadToCache(f, imageName[-1], caller='star')

        return message.message(file='cache/star_' + imageName[-1])

    # Goldfish
    if message_in.command == 'goldfish':
        try:
            f = urllib.request.urlopen("http://goldfishapi.azurewebsites.net/goldfish/rand.php").read().decode("utf-8")
        except urllib.error.URLError as e:
            return message.message(body='There was an issue connecting to goldfish API.'.format(message_in.body))

        imageName = f.split('/')
        caching.downloadToCache(f, imageName[-1], caller='goldfish')

        return message.message(file='cache/goldfish_' + imageName[-1])
