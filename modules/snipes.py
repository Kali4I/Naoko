import discord
from discord.ext import commands

from collections import deque
from random import randint as rint

class SnipeHistory(deque):
    def __init__(self):
        super().__init__(maxlen=5)

    def __repr__(self):
        return "Naoko Snipe History"

class Snipes():
    """Snipe anything deleted"""
    def __init__(self, bot):
        self.bot = bot
        self.snipes = {}
        self.thumbnail = self.bot.user.avatar_url
        
    def cleanup(self):
        """Function to clean up snipe cache"""
        self.snipes = {}
    
    async def on_message_delete(self, message):
        """Event is triggered when message is deleted"""
        if message.channel.is_nsfw():
            return
        
        try:
            self.snipes[message.channel.id].appendleft(message)
        except:
            self.snipes[message.channel.id] = SnipeHistory()
            self.snipes[message.channel.id].appendleft(message)
        
    @commands.command()
 #   @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def snipe(self, ctx, channel: discord.TextChannel = None, index: int = 0):
        
        channel = channel or ctx.channel

        if index != 0:
            index = index-1

        if channel.is_nsfw():
            await ctx.send('Attempting to snipe a NSFW channel')

        else:
            try:
                sniped = self.snipes[channel.id][index]
            except:
                await ctx.send(':warning: | **Index must not be greater than 5 or lesser than 1**', delete_after=10)
            else:
                embed=discord.Embed(color=rint(0x000000, 0xFFFFFF), timestamp=sniped.created_at, title=f"@{sniped.author} said in #{sniped.channel}", description=sniped.clean_content)
                embed.set_footer(text=f"Sniped by {ctx.author.name} | Message created", icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=sniped.author.avatar_url)
                await ctx.send(embed=embed)
 
def setup(bot):
    bot.add_cog(Snipes(bot))
