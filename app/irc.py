import irc.client
import irc.bot

import asyncio
import threading

from app.logging import Ansi
from app.logging import log

import app.state.sessions as session

loop = 0
irc_gateway = 0

class IrcGateway(irc.client.SimpleIRCClient):
    def __init__(self):
        irc.client.SimpleIRCClient.__init__(self)
        self.targets = session.channels
    
    def on_welcome(self, c, e):
        for channel in self.targets:
            if irc.client.is_channel(channel.name):
                log(f"IRC: Joining channel {channel.name}", Ansi.LGREEN)
                c.join(channel.name)
    
    def on_pubmsg(self, c, e):
        log(f"IRC: {e.source.nick}: {e.arguments[0]}", Ansi.LGREEN)
        global loop
        self.future = asyncio.ensure_future(
            self.transmit_message_to_osu(e.arguments[0], e.source.nick, e.target), loop=loop
        )

    async def transmit_message_to_osu(self, message, sender, target):
        target_channel = session.channels.get_by_name(target)
        if target_channel is None:
            return
        player = await session.players.from_cache_or_sql(name=sender)
        if player is None:
            return
        
        target_channel.send(message, player)
        if player.is_online and not player.is_bot_client:
            player.send(message, player, target_channel)

    def transmit_message_to_irc(self, message, sender, target):
        # TODO: help??? ;_;
        #self.connection.privmsg(target.name, message)
        pass

def irc_thread(irc_gateway : IrcGateway):
    try:
        irc_gateway.connect(server='192.168.1.31', port=6667, nickname='testBOT')
    except irc.client.ServerConnectionError as x:
        log(x, Ansi.RED)
    
    log("IRC: BOT started", Ansi.LGREEN)
    
    try:
        irc_gateway.start()
    finally:
        irc_gateway.connection.disconnect()

def start_irc_handler():
    log("IRC: Starting BOT", Ansi.LGREEN)
    global irc_gateway
    irc_gateway = IrcGateway()
    global loop
    loop = asyncio.get_event_loop()
    
    thread = threading.Thread(target=irc_thread, args=(irc_gateway,))
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



    
    

    