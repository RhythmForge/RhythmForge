import irc.client
import irc.bot
import irc.client_aio

import asyncio
import threading

from app.logging import Ansi
from app.logging import log

from typing import TYPE_CHECKING

import app.state
from app.repositories import channels as channel_repo
from app.objects.player import Player
if TYPE_CHECKING:
    from app.objects.channel import Channel

class IrcGateway(irc.client.SimpleIRCClient):
    def __init__(self, target):
        irc.client.SimpleIRCClient.__init__(self)
        self.target = target
    
    def on_welcome(self, c, e):
        log("IRC: Joining channel", Ansi.LGREEN)
        if irc.client.is_channel(self.target):
            c.join(self.target)
    
    def on_pubmsg(self, c, e):
        log("IRC: Message rcvd", Ansi.LGREEN)
        self.transmit_message(e.arguments[0], 'snabbis', '#osu')
        # tomorrow: use ensure_future to call async transmit_message and pull name from db

    def transmit_message(self, message, sender, target):
        target_channel = app.state.sessions.channels.get_by_name(target)
        player = app.state.sessions.players.get(name=sender)
        if player is not None:
            target_channel.send(message, player)
            if player.is_online:
                player.send(message, player, target_channel)

def irc_thread():
    irc_client = IrcGateway('#osu')
    
    try:
        irc_client.connect(server='192.168.1.31', port=6667, nickname='testBOT')
    except irc.client.ServerConnectionError as x:
        log(x, Ansi.RED)
    
    log("IRC: BOT started", Ansi.LGREEN)
    
    try:
        irc_client.start()
    finally:
        irc_client.connection.disconnect()

def start_irc_handler():
    log("IRC: Starting BOT", Ansi.LGREEN)
    global loop
    loop = asyncio.get_event_loop()
    thread = threading.Thread(target=irc_thread)
    thread.daemon = True
    thread.start()
    
    

# add 'on_' to every protocol to receive data as functions
# protocol = [
#     "error",
#     "join",
#     "kick",
#     "mode",
#     "part",
#     "ping",
#     "privmsg",
#     "privnotice",
#     "pubmsg",
#     "pubnotice",
#     "quit",
#     "invite",
#     "pong",
#     "action",
#     "topic",
#     "nick",
# ]



    
    

    