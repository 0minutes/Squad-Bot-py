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
from nextcord import Embed, Member, bans, Colour
from nextcord.ui import Button, View
from nextcord.ext import commands
from datetime import timedelta, datetime
from PIL import Image
from io import BytesIO
from nextcord.utils import get

config = {
    'token': 'MTAyNzk4OTMwNTMyMDI5NjQ1OA.GViMtU.zmaH3mvtpy-_Ge_P1GLTG2mluN60WbuMLkv2mo',
    'prefix': '.',
}

intents =  intents = nextcord.Intents().all()

bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"""Logged in as "{bot.user}"
LOGS:""")

##HELP COMMAND
bot.remove_command("help")

@bot.command(name="help")
async def help(ctx):
    embed = Embed(color=0x2F3136, title="Basic Commands List")
    embed.add_field(name=".roll (1 100)", value="get a random number 1 - 100, can also be anything you like by just doing .roll 1 10", inline=False)
    embed.add_field(name=".guess", value="Can try and guess a number between 1 and 100 with 5 attempts.(you will be getting hits)", inline=False)
    embed.add_field(name=".hi", value="if you're feeling lonely bot replies with hi", inline=False)
    embed.add_field(name=".howgay", value="The bots predicts how gay you are", inline=False)
    embed.add_field(name=".socials", value="Gives you a list of my socials", inline=False)
    embed.add_field(name=".profile (@user)", value="lets you see your profile and others!", inline=False)
    embed.add_field(name=".server", value="lets you see servers profile!", inline=False)
    embed.add_field(name=".generate", value="Generates images (Powered by craiyon.com)", inline=False)
    embed.add_field(name=".createvoice", value="You can create and edit a voice channel with - .createvoice name, user limit, bitrate exapmle .createvoice Help_Example 5 128 make sure the name is one singular word. The channel deletes itself after 24hours!", inline=False)
    embed.add_field(name="**.helpM**", value="**Moderation Help**", inline=False)
    embed.add_field(name="**valorant**", value="**Valorant Commands Help**", inline=False)
    await ctx.reply(embed=embed)


### MODERATION HELP
@bot.command(name="helpM")
async def helpM(ctx):
    embed = Embed(color=0x2F3136, title="Moderation Commands List")
    embed.add_field(name=".ban", value="ban members of the server/guild", inline=False)
    embed.add_field(name=".kick", value="kicks a server member", inline=False)
    embed.add_field(name=".clear + amount", value="clears the ammount that you've set!", inline=False)
    await ctx.reply(embed=embed)

## !!!VALROANT!!! ###
##VAL HELP

@bot.command(name="valorant")
async def valorant(ctx):
    embed = Embed(color=0x2F3136, title="Valorant Help")
    embed.add_field(name=".tier + tier level", value="tells you how much XP the tier requires", inline=False)
    await ctx.reply(embed=embed)

@bot.command(name="tier")
async def tier(ctx, tier:int, max=50, defualt=1, BPfinishEpilogue = 1162500, BPfinish = 980000):
    ## IF TIER IS LOWER THAN 50 DO THE CALCULATION
    if tier <= max:
        xp = int(tier) * 750 + 500
        TierLog = print(f"TierLog: {tier}")
        ##totalxp = 
        await ctx.reply(f"tier {tier} requires {xp}XP")
    ### ELSE REPLY WITH - 
    else:
        await ctx.reply("After tier 50 to 55 takes 36500XP")
##IF NO TIER LVL DISPLAY THIS MSG -
@tier.error
async def tier_error(ctx:commands.Context, error: commands.CommandError):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.reply(f"tier is missing an argument")
        return

###----------------------------------------------------------------------------!!!CASUAL COMMANDS!!!-----------------------------------------------------------------------###

##INFO
@bot.command(name="profile")
async def Profile(ctx, user: Member=None):

    if user == None:
        user = ctx.message.author
    inline = True
    embed = Embed(title=user.name+"#"+user.discriminator, color=0x2F3136)
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

@bot.command(name="server")
async def Server(ctx):
    guild = ctx.message.author.guild
    embed = Embed(title=guild.name, color=0x2F3136)
    serverData = {
        "Owner" : guild.owner.mention,
        "Channels" : len(guild.channels),
        "Categories" : len(guild.categories),
        "Members" : guild.member_count,
        "Roles" : guild.role_count,
        "Created at" : guild.created_at.strftime("%b %d, %Y, %T"),
        "Description" : guild.description,
    }
    for [fieldName, fieldVal] in serverData.items():
            embed.add_field(name=fieldName+":", value=fieldVal, inline=True)
    embed.set_footer(text=f"id: {guild.id}")

    embed.set_thumbnail(guild.icon)
    await ctx.reply(embed=embed)

##TEST CREATE VC
@bot.command(name="createvoice")
async def createvoice(ctx, name="Custom Voice", user_limit = int(5), bitrate = int(64)):
    user = ctx.message.author
    guild = ctx.message.author.guild
    category = get(guild.categories, name="Custom VCs")
    channel = await guild.create_voice_channel(name=name, user_limit=user_limit, category = category, bitrate = bitrate * 1000)
    embed = Embed(color=0x2F3136, description=f"{name} VC was made with the user limit being {user_limit} and bitrate of {bitrate} by <@{user.id}> ")
    embed.set_author(name=f"{name} VC", url="https://cdn.discordapp.com/emojis/947101075981340713.webp?size=96&quality=lossless")
    embed.set_footer(text="Comlpleted successfully")
    await ctx.send(embed=embed)
    time.sleep(86400)
    await channel.delete()

##INVITE COMMAND!
@bot.command("invite")
async def invite(ctx):
    await ctx.reply("Here is a link to my discord server! - https://discord.gg/vbNjVExh77")

##GENERATOR 

@bot.command(name="generate")
async def generate(ctx: commands.context, *, prompt: str):
    ETA = int(time.time() + 60)
    msg = await ctx.send(f"Go grab a coffee, this may take a while :D... ETA: <t:{ETA}:R>")
    generator = Craiyon()
    endResult = generator.generate(prompt)
    images = endResult.images
    GenLog = print(f'GenLog: "{prompt}"')
    for i in images:
        image = BytesIO(base64.decodebytes(i.encode("utf-8")))
        return await msg.edit(content="Image Generated! Make sure to visit **https://www.craiyon.com/** if ur cool :>", file = nextcord.File(image, f"{prompt}.png"))


## Hi COMMAND
@bot.command(name="hi")
async def hi(ctx):
    await ctx.reply("Hello there! :D")

##arkyhh
Arkyhhs = ["Arkyhh :smirk:", "Arkyhh lookin' sus :face_with_open_eyes_and_hand_over_mouth:", "Arkyhh go stupid go crazy balalalala", "Feet pics from Arkyhh at https://www.gegudkiddo.com","proof that earth is flat compiled by Arkyhh: https://www.youtube.com/watch?v=fF6T7GWPygk","Cool PC tricks by Akryhh number one : delete folder named syst...","Arkyhh when he get's a good skin in his shop - :no_entry_sign: :money_with_wings:"]
@bot.command(name="Arkyhh")
@commands.cooldown(1, 30, commands.BucketType.user)
async def Arkyhh(ctx):
    await ctx.send(random.choice(Arkyhhs))

@Arkyhh.error
async def Arkyhh_error(ctx:commands.Context, error: commands.errors.CommandOnCooldown):
    if isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.reply(f"You can only use this command once every 30 socends, Try again in {error.retry_after:.2f}s")
        return

##playlist command

@bot.command(name="connect")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command(name="disconnect")
async def leave(ctx):
    await ctx.voice_bot.disconnect()


## Say command

@bot.command(name="say")
async def say(ctx, *, message):
    ## DELETE ORIGINAL MSG
    await ctx.message.delete()
    ## SEND ORIGINAL MSG
    await ctx.send(f"{message}")

##ROLL COMMAND
@bot.command(name='roll')
async def roll(ctx, min='1', max='100'): 
    RollLog = print(f"RollLog: Min {min} - Max {max}")
    print(RollLog)
    await ctx.reply(random.randint(int(min), int(max)))

##GUESS COMMAND
@bot.command(name="guess")
@commands.cooldown(1, 60, commands.BucketType.user)
async def guess(ctx):
    await ctx.reply("I thought of a number between **1 and 100, You got 5 guesses good luck!**")
    guesses = 5
    num = random.randint(1, 100)
    GuessLog = print(f"GuessLog: {num}")
    while True:
        msg = await bot.wait_for('message',check=lambda m:m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
        guesses-=1
        num_ = int(msg.content)
        if num!=num_:
            await ctx.send(f"Incorrect! The number that I chose is {'**higher**' if num_<num else '**lower**'} you have *{guesses} guesses left*")
        else:
            await ctx.send(f"Correct! You guessed the number in **{5 - guesses} guesses!**")
            break
        if guesses == 0:
            await ctx.send(f"Incorrect! The number that I chose was **{num}**, better luck next time")
            break
## GUESS ERROR
@guess.error
async def Guess_error(ctx:commands.Context, error: commands.errors.CommandOnCooldown):
    if isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.reply(f"You can only use this command once every 60 socends, Try again in {error.retry_after:.2f}s")
        return


## HOW GAY

@bot.command(name="howgay")
async def howgay(ctx, member: nextcord.Member):
    await ctx.reply(f"{member.mention} is {random.randint(1, 100)}% :rainbow:")

##SOCIALS COMMAND
@bot.command(name="socials")
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

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        message = f"Welcome {member.mention} to {guild.name}. Make sure you check you #rules , bot prefix is '.' hopefully you will enjoy it here!"
        await guild.system_channel.send(message)
    role = nextcord.utils.get(message.guild.roles, name = "Squad")
    await bot.add_role(member, role)


#### ------------------------------------------------------------------------------!!!MODERATION!!!-------------------------------------------------- ###
class verify(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        self.value = None
    
    @nextcord.ui.button(label="Verify", style=nextcord.ButtonStyle.success)
    async def demo1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role = 1043845192266031105
        user = interaction.user
        await user.add_roles(user.guild.get_role(role))
        await interaction.response.send_message("Successfully verified!", ephemeral=True)
    
##VERIFY
@commands.guild_only()
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
@bot.command(name="verify")
async def Verify(ctx):
    embed = Embed(color=0x2F3136, description="""Make sure you read the server <#1028421022204051556>. For any help message the owner <@692430762896523406> \n
    For bot help do .help and make sure to have fun!\n
    To Verify Click the button below :arrow_down:\n""")
    embed.set_author(name="SquadBot Verify", url="https://cdn.discordapp.com/emojis/947101075981340713.webp?size=96&quality=lossless")
    embed.set_footer(text=f"• Made By 0minutes")
    await ctx.send(embed=embed, view = verify())

##RULES
@commands.guild_only()
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
@bot.command(name="rules")
async def rules(ctx):
    embed = Embed(color=0x2F3136, description="""**・1. Be respectful**\n You must respect all users, regardless of your liking towards them. Treat others the way you want to be treated.\n
    **・2. No Inappropriate Language**\n The messages with innapropriate words will be automatically removed. However, any derogatory language towards any user is prohibited.\n
    **・3. No spamming**\n Don't send a lot of small messages right after each other. Do not disrupt chat by spamming.\n
    **・4. No adult/NSFW material**\n This is a friendly server and not meant to share this kind of material.\n
    **・5. No offensive names and profile pictures**\n You will be asked to change your name or picture if the staff deems them inappropriate.\n
    **・6. Server Raiding**\n Raiding or mentions of raiding are not allowed.\n
    **・7. Direct & Indirect Threats**\n Threats to other users of DDoS, Death, DoX, abuse, and other malicious threats are absolutely prohibited and disallowed\n
    **・8. Respect Staff team and members** Please respect the staff team as they are here to help you and guide you through our bot and respect the members and not get yourself in trouble.\n
    **・9. Follow the Discord Community Guidelines And TOS**\n You can find them here:\n https://discordapp.com/guidelines\n  https://discord.com/TOS\n \n""")
    embed.set_author(name="SquadBot Server rules", url="https://cdn.discordapp.com/emojis/947101075981340713.webp?size=96&quality=lossless")
    embed.set_footer(text="• Rules By 0minutes#0201")
    await ctx.send(embed=embed)
##WORD FILTER

bad_words = ["bad_test","cunt","fk u","fuck","fuck u","fuck you","dick head","nigger","nga","nigga","paki","dumbass","gay sex","jerk off","KKK","retard","wanker","boobs","titties","tits","tit","https://www.pornhub.com","pornhub","porn","pedophile"]

##Checkes the message
@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    msg_content = message.content.lower()
    
    # delete curse word if match with the list
    if any(word in msg_content for word in bad_words):
        await message.delete()
        await message.channel.send("Dont say that again!")
    await bot.process_commands(message)

##.CLEAR COMMAND
@commands.guild_only()
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
@bot.command(name="clear")
async def clear(ctx, amount=5):    
    await ctx.channel.purge(limit=amount+1)

##UNBAN

##BAN COMMAND
@bot.command(name="ban")
@commands.guild_only()
@commands.has_permissions(ban_members = True)
@commands.bot_has_permissions(ban_members = True)
async def ban(ctx:commands.Context, member: Member, *, reason:str=None):
    if reason == None:
        reason = "No reason provided"

    await member.ban(delete_message_days=0, reason=reason)
    await ctx.reply(f"**{member.name} is banned for {reason}**")

##KICK COMMAND
@bot.command(name="kick")
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

bot.run(config["token"])