# Creates a comment that can scroll through a list, controllable via buttons
# PREAMBLE ####################################################################
import discord
import asyncio

from discord.ext import commands
from . import listener

class Scrollable(listener.RctListener):
    """Creates a comment that can scroll through a list, controllable via buttons"""
    def __init__(self, bot):
        # Create the message
        self.bot = bot
        self.msg_list = None
        self.cur_pos = 0
        self.msg = None # TODO: aghh pylint stop it
        super().__init__(None)    # TODO: I screwed up somewhere with designing this

    @asyncio.coroutine
    def send(self, channel, msg_list, cur_pos=0):
        """Send the given message list, scrolled to the given position"""
        print("Send begin")
        self.msg = yield from self.bot.send_message(channel, msg_list[cur_pos])
        self.bot.add_reaction(self.msg, ":arrow_up_small:")
        self.bot.add_reaction(self.msg, ":arrow_down_small:")
        self.msg_list = msg_list
        self.cur_pos = cur_pos
        self.attach(channel)
        print("Send end")

    async def on_reaction(self, rct):
        """Handle the scroll reaction"""
        if str(rct) == ":arrow_up_small:":
            self.cur_pos += 1
        elif str(rct) == ":arrow_down_small:":
            self.cur_pos -= 1
        print("reaction: " + str(rct))   # Debugging code
        self.bot.edit_message(self.msg, self.msg_list[self.cur_pos])
