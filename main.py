import base64
import nextcord
import asyncio
import aiosqlite
import random
import json
import os
import datetime 
import humanfriendly
import time
from craiyon import Craiyon
from nextcord import Embed, Member, bans, colour
from nextcord.ui import Button, View
from nextcord.ext import commands
from datetime import timedelta, datetime
from PIL import Image
from io import BytesIO
from nextcord.utils import get


intents = nextcord.Intents().all()
client = commands.Bot(command_prefix=".", intents=intents)



##HELP COMMAND
client.remove_command("help")

@client.command(name="help")
async def help(ctx):
    embed = Embed(color=0xab1111, title="Basic Commands List")
    embed.add_field(name=".roll", value="get a random number 1 - 100", inline=False)
    embed.add_field(name=".hi", value="bot replies with hi", inline=False)
    embed.add_field(name=".howgay", value="The bots predicts how gay you are", inline=False)
    embed.add_field(name=".socials", value="Gives you a list of my socials", inline=False)
    embed.add_field(name=".profile (@user)", value="lets you see your profile and others!", inline=False)
    embed.add_field(name=".server", value="lets you see servers profile!", inline=False)
    embed.add_field(name=".generate", value="Generates images (Powered by craiyon.com)", inline=False)
    embed.add_field(name="**.helpM**", value="**Moderation Help**", inline=False)
    embed.add_field(name="**valorant**", value="**Valorant Commands Help**", inline=False)
    await ctx.reply(embed=embed)

### MODERATION HELP
@client.command(name="helpM")
async def helpM(ctx):
    embed = Embed(color=0x780200, title="Moderation Commands List")
    embed.add_field(name=".ban", value="ban members of the server/guild", inline=False)
    embed.add_field(name=".kick", value="kicks a server member", inline=False)
    embed.add_field(name=".clear + amount", value="clears the ammount that you've set!", inline=False)
    await ctx.reply(embed=embed)

## !!!VALROANT!!! ###
##VAL HELP

@client.command(name="valorant")
async def valorant(ctx):
    embed = Embed(color=0xdc3d4b, title="Valorant Help")
    embed.add_field(name=".tier + tier level", value="tells you how much XP the tier requires", inline=False)
    await ctx.reply(embed=embed)


@client.command(name="tier")
async def tier(ctx, tier:int, max=50, defualt=1, BPfinishEpilogue = 1162500, BPfinish = 980000):
    ## IF TIER IS LOWER THAN 50 DO THE CALCULATION
    if tier <= max:
        xp = int(tier) * 750 + 500
        ##totalxp = 
        await ctx.reply(f"tier {tier} requires {xp}XP")
    ### ELSE REPLY WITH - 
    else:
        await ctx.reply("After tier 50 to 55 takes 36500XP")

@tier.error
async def tier_error(ctx:commands.Context, error: commands.CommandError):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply(f"tier is missing an argument")
        return

### !!!CASUAL COMMANDS!!! ###

##INFO

@client.command(name="profile")
async def Profile(ctx, user: Member=None):

    if user == None:
        user = ctx.message.author
    inline = True
    embed = Embed(title=user.name+"#"+user.discriminator, color=0xab1111)
    userData = {
        "Mention" : user.mention,
        "Nick" : user.nick, 
        "Created at" : user.created_at.strftime("%b %d, %Y, %T"),
        "Joined at" : user.joined_at.strftime("%b %d, %Y, %T"),
        "Server" : user.guild,
        "Top Role" : user.top_role
    }
    for [fieldName, fieldVal] in userData.items():
        embed.add_field(name=fieldName+":", value=fieldVal, inline=inline)
    embed.set_footer(text=f"id: {user.id}")

    embed.set_thumbnail(user.display_avatar)
    await ctx.reply(embed=embed)

@client.command(name="server")
async def Server(ctx):
    guild = ctx.message.author.guild
    embed = Embed(title=guild.name, color=0xab1111)
    serverData = {
        "Owner" : guild.owner.mention,
        "Channels" : len(guild.channels), 
        "Members" : guild.member_count,
        "Created at" : guild.created_at.strftime("%b %d, %Y, %T"),
        "Description" : guild.description,
    }
    for [fieldName, fieldVal] in serverData.items():
            embed.add_field(name=fieldName+":", value=fieldVal, inline=True)
    embed.set_footer(text=f"id: {guild.id}")

    embed.set_thumbnail(guild.icon)
    await ctx.reply(embed=embed)

##INVITE COMMAND!
@client.command("invite")
async def invite(ctx):
    await ctx.reply("Here is a link to my discord server! - https://discord.gg/vbNjVExh77")

@client.command(name="generate")
async def generate(ctx: commands.context, *, prompt: str):
    ETA = int(time.time() + 60)
    msg = await ctx.send(f"Go grab a coffee, this may take a while :D... ETA: <t:{ETA}:R>")
    generator = Craiyon()
    endResult = generator.generate(prompt)
    images = endResult.images
    for i in images:
        image = BytesIO(base64.decodebytes(i.encode("utf-8")))
        return await msg.edit(content="Image Generated! Make sure to visit **https://www.craiyon.com/** if ur cool :>", file = nextcord.File(image, f"{prompt}.png"))

## Hi COMMAND
@client.command(name="hi")
async def hi(ctx):
    await ctx.reply("Hello there! :D")

## Say command

@client.command(name="say")
async def say(ctx, *, message):
    ## DELETE ORIGINAL MSG
    await ctx.message.delete()
    ## SEND ORIGINAL MSG
    await ctx.send(f"{message}")

##ROLL COMMAND
@client.command(name="roll")
async def Random(ctx, min, max):
    min = int(min)
    max = int(max)
    await ctx.reply(random.randint(min, max))

##GUESS COMMAND
##@client.command(name="guess")
##async def Random(ctx, *, message):
##    await ctx.reply("I thought of a number between **1 and 100**")
##    guesses = 5
##    TheGuess = int(message)
##    num = random.randint(1, 100)
##
##    if TheGuess == num:
##        await ctx.reply(f"{TheGuess} was the the number I guessed! Good Job!")
##    if TheGuess > num:
##        await ctx.reply(f"The number that you have guesses is **higher** than the one I guessed. **You have {guesses - 1} attempts left**")
##    if TheGuess < num:
##        await ctx.reply(f"The number that you have guesses is **lower** than the one I guessed. **You have {guesses - 1} attempts left**")
##    if guesses == 0:
##        await ctx.reply(f"You have no more guesses left ): Unlcuky")

## HOW GAY

@client.command(name="howgay")
async def howgay(ctx, member: nextcord.Member):
    await ctx.reply(f"{member.mention} is {random.randint(1, 100)}% :rainbow:")

##SOCIALS COMMAND
@client.command(name="socials")
async def socials(ctx):
    Twitch = Button(label="Twitch", url="https://www.twitch.tv/0minutesval")
    Youtube = Button(label="Youtube", url="https://www.youtube.com/channel/UC4IZby3-37G0sZO0ZSDmCKg")
    FriendTwitch = Button(label="Friends Twitch", url="https://www.twitch.tv/tvkrano")
    Discord = Button(label="My Discord Server!", url="https://discord.gg/vbNjVExh77")

    myview = View(timeout=240)
    myview.add_item(Twitch)
    myview.add_item(Youtube)
    myview.add_item(FriendTwitch)
    myview.add_item(Discord)

    await ctx.reply("Twitch And Youtube! Make sure to follow and give me a sub ;) + my friend's twitch!", view=myview)

##WELCOME 

@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        message = f"Welcome {member.mention} to {guild.name}. Make sure you check you #rules, bot prefix is '.' hopefully you will enjoy it here!"
        await guild.system_channel.send(message)
    role = nextcord.utils.get(message.guild.roles, name = "Squad")
    await client.add_role(member, role)


#### !!!MODERATION!!! ###

##RULES 
@commands.guild_only()
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
@client.command(name="rules")
async def rules(ctx):
    embed = Embed(color=0xab1111, title="`Rules`")
    embed.add_field(name="`1. Be respectful`", value="You must respect all users, regardless of your liking towards them. Treat others the way you want to be treated.")
    embed.add_field(name="`2. No Inappropriate Language`", value="The messages with innapropriate words will be automatically removed. However, any derogatory language towards any user is prohibited.")
    embed.add_field(name="`3. No spamming`", value="Don't send a lot of small messages right after each other. Do not disrupt chat by spamming.")
    embed.add_field(name="`4. No adult/NSFW material`", value="This is a friendly server and not meant to share this kind of material.")
    embed.add_field(name="`5. No offensive names and profile pictures`", value="You will be asked to change your name or picture if the staff deems them inappropriate.")
    embed.add_field(name="`6. Server Raiding`", value="Raiding or mentions of raiding are not allowed.")
    embed.add_field(name="`7. Direct & Indirect Threats`", value="Threats to other users of DDoS, Death, DoX, abuse, and other malicious threats are absolutely prohibited and disallowed.")
    embed.add_field(name="`8. Follow the Discord Community Guidelines And TOS`", value="You can find them here: https://discordapp.com/guidelines and TOS: https://discord.com/TOS")
    embed.add_field(name="`9. Enjoy`", value="Enjoy your stay here and have fun!")
    await ctx.send(embed=embed)

##WORD FILTER

bad_words = ["bad_test","cunt","fk u","fuck","fuck u","fuck you","dick head","nigger","nga","nigga","paki","dumbass","gay sex","jerk off","KKK","retard","wanker","boobs","titties","tits","tit","https://www.pornhub.com","pornhub","porn","pedophile"]


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    msg_content = message.content.lower()
    
    # delete curse word if match with the list
    if any(word in msg_content for word in bad_words):
        await message.delete()
        await message.channel.send("Dont say that again!")
    await client.process_commands(message)

##.CLEAR COMMAND
@commands.guild_only()
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
@client.command(name="clear")
async def clear(ctx, amount=5):    
    await ctx.channel.purge(limit=amount+1)

##UNBAN

##BAN COMMAND
@client.command(name="ban")
@commands.guild_only()
@commands.has_permissions(ban_members = True)
@commands.bot_has_permissions(ban_members = True)
async def ban(ctx:commands.Context, member: Member, *, reason:str=None):
    if reason == None:
        reason = "No reason provided"

    await member.ban(delete_message_days=0, reason=reason)
    await ctx.reply(f"**{member.name} is banned for {reason}**")

##KICK COMMAND
@client.command(name="kick")
@commands.guild_only()
@commands.has_permissions(kick_members = True)
@commands.bot_has_permissions(kick_members = True)
async def kick(ctx, member : nextcord.Member, *, reason=None):
    if reason == None:
        reason = "No reason provided"
    
    await member.kick(reason=reason)
    await ctx.reply(f"**{member.name} is kicked for {reason}**")

### !!!ERROR HANDLER!!! ###

##KICK ERROR
@kick.error
async def kick_error(ctx:commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(f"you do not have the kick members premissions")
        return
    
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.reply(f"I dont have premissions to do that!")
        return

#BAN ERROR
@ban.error
async def ban_error(ctx:commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(f"you do not have the ban members premissions")
        return
    
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.reply(f"I dont have premissions to do that!")
        return

##CLEAR ERROR
@clear.error
async def clear_error(ctx:commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(f"you do not have the manage messages premissions!")
        return
    
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.reply(f"I dont have premissions to do that!")
        return

##RULES ERROR
@rules.error
async def rules_error(ctx:commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(f"you do not have the manage messages premissions!")
        return
    
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.reply(f"I dont have premissions to do that!")
        return

client.run("MTAyNzk4OTMwNTMyMDI5NjQ1OA.GNz7mp.elHqewsbrKeG41EhPYzUqyXIh5cb-OzEnpHmgo")