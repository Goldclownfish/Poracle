#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from disco.bot import Plugin
from disco.types import channel
from disco.util.sanitize import S
from utils.args import args as get_args
from utils.geo import geoloc
from utils.mysql import registered, register, unregister, activate, deactivate, registered_by_name, set_location

args = get_args(os.path.abspath(os.path.dirname(__file__)))

class Commands(Plugin):

## Register DM id as human
    @Plugin.command('register')
    def command_register(self, event):
        dmid = event.msg.author.open_dm().id
        name = event.msg.author
        ping = event.msg.author.mention
        if not (event.msg.channel.is_dm):
            if (event.msg.channel.name == args.channel):
                if not(registered(dmid)):
                    register(dmid,name)
                    event.msg.reply('Hello {}, thank you for registering!'.format(ping))
                else:
                    event.msg.reply('Hello {}, you are already registered'.format(ping))
            else:
                event.msg.reply(
                    'Hello {}, !register is only available in #{}'.format(ping, args.channel))


## Unregister humans DM id
    @Plugin.command('unregister')
    def command_unregister(self, event):
        if not (event.msg.channel.is_dm):
            if (event.msg.channel.name == args.channel):
                dmid = event.msg.author.open_dm().id
                ping = event.msg.author.mention
                if not (registered(dmid)):
                    event.msg.reply(
                        'Hello {}, You are not currenlty registered!'.format(ping))
                else:
                    unregister(dmid)
                    event.msg.reply(
                        'Hello {}, You are no longer registered!'.format(ping))

## Enable alarms for human
    @Plugin.command('start')
    def command_start(self, event):
        dmid = event.msg.author.open_dm().id
        ping = event.msg.author.mention
        name = event.msg.author
        if (event.msg.channel.is_dm):
            if (registered_by_name(name)):
                activate(dmid)
                event.msg.reply('Your alarms have been activated!')
            else:
                event.msg.reply(
                    'This command is only available for registered humans! :eyes:')
        else:
            event.msg.reply('Hello {}, This command is only available in DM '.format(ping))


## Disable alarms for human
    @Plugin.command('stop')
    def command_stop(self, event):
        dmid = event.msg.author.open_dm().id
        ping = event.msg.author.mention
        name = event.msg.author
        if (event.msg.channel.is_dm):
            if (registered_by_name(name)):
                deactivate(dmid)
                event.msg.reply('Your alarms have been stopped!')
            else:
                event.msg.reply(
                    'This command is only available for registered humans! :eyes:')
        else:
            event.msg.reply('Hello {}, This command is only available in DM '.format(ping))

## Set Humans Location
    @Plugin.command('location', '<content:str...>')
    def command_location(self, event, content):
        name = event.msg.author
        ping = event.msg.author.mention
        content = content.encode('utf-8')
        if (event.msg.channel.is_dm):
            if not (registered_by_name(name)):
                event.msg.reply(
                    'This command is only available for registered humans! :eyes:')
            else:
                loc = geoloc(content)
                if (loc == 'ERROR'):
                    event.msg.reply(
                        'I was unable to locate {}'.format(content))
                else:
                    set_location(name,loc[0],loc[1])
                    event.msg.reply(
                        'I Have set your location to {}'.format(content))
        else:
            event.msg.reply(
                'Hello {}, This command is only available in DM '.format(ping))


## Set tracking for monster