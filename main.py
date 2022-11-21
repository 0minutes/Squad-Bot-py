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
from nextcord.ext import commands, application_checks
from datetime import timedelta, datetime
from PIL import Image
from io import BytesIO
from nextcord.utils import get
import nextcord, asyncio, aiosqlite, humanfriendly
from datetime import datetime
from nextcord import Interaction, ChannelType, SlashOption
from nextcord.ext import commands, tasks, application_checks
from nextcord.abc import GuildChannel
from datetime import datetime


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

@bot.slash_command(name="help", description="Bot's commands!")
async def help(interaction: nextcord.Interaction):
    embed = Embed(color=0x2F3136, title="Basic Commands List")
    embed.add_field(name="roll", value="get a random number 1 - 100, can also be anything you like by just doing .roll 1 10", inline=False)
    embed.add_field(name="guess", value="Can try and guess a number between 1 and 100 with 5 attempts.(you will be getting hits)", inline=False)
    embed.add_field(name="socials", value="Gives you a list of my socials", inline=False)
    embed.add_field(name="profile (@user)", value="lets you see your profile and others!", inline=False)
    embed.add_field(name="server", value="lets you see servers profile!", inline=False)
    embed.add_field(name="generate", value="Generates images (Powered by craiyon.com)", inline=False)
    embed.add_field(name="createvoice", value="You can create and edit a voice channel with - .createvoice name, user limit, bitrate exapmle .createvoice Help_Example 5 128 make sure the name is one singular word. The channel deletes itself after 24hours!", inline=False)
    embed.add_field(name="ban", value="ban members of the server/guild", inline=False)
    embed.add_field(name="kick", value="kicks a server member", inline=False)
    embed.add_field(name="purge + amount", value="clears the ammount that you've set!", inline=False)
    await interaction.send(embed=embed)


###----------------------------------------------------------------------------!!!CASUAL COMMANDS!!!-----------------------------------------------------------------------###

##INFO
@bot.slash_command(name="profile")
async def Profile(interaction: nextcord.Interaction, user: Member=None):

    if user == None:
        user = interaction.user
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
    await interaction.send(embed=embed)

@bot.slash_command(name="server")
async def Server(interaction: nextcord.Interaction):
    guild = interaction.guild
    embed = Embed(title=guild.name, color=0x2F3136)
    serverData = {
        "Owner" : guild.owner.mention,
        "Channels" : len(guild.channels),
        "Categories" : len(guild.categories),
        "Members" : guild.member_count,
        "Created at" : guild.created_at.strftime("%b %d, %Y, %T"),
        "Description" : guild.description,
    }
    for [fieldName, fieldVal] in serverData.items():
            embed.add_field(name=fieldName+":", value=fieldVal, inline=True)
    embed.set_footer(text=f"id: {guild.id}")

    embed.set_thumbnail(guild.icon)
    await interaction.send(embed=embed)

## CREATE VC
@bot.slash_command(name="createvoice", description="allows you to create a voice channel that will delete itself in 24hrs")
async def createvoice(interaction: nextcord.Interaction, name="Custom Voice", user_limit = int(5)):

    user = interaction.user
    guild = interaction.guild
    category = get(guild.categories, name="Custom VCs")
    channel = await guild.create_voice_channel(name=name, user_limit=user_limit, category = category)
    embed = Embed(color=0x2F3136, description=f"{name} VC was made with the user limit being {user_limit} by <@{user.id}> ")
    embed.set_author(name=f"{name} VC", url="https://cdn.discordapp.com/emojis/947101075981340713.webp?size=96&quality=lossless")
    embed.set_footer(text="Comlpleted successfully")
    await interaction.send(embed=embed)
    time.sleep(86400)
    await channel.delete()

@bot.slash_command(name="disconnect", description="disconnects a user from your custom voicechat")
async def disconnect(interaction: nextcord.Interaction, member: Member):
    channel = interaction.user.voice.channel
    interaction.channel.member.disconnect()

##GENERATOR 

@bot.slash_command(name="generate")
async def generate(interaction: nextcord.Interaction, *, prompt: str):
    ETA = int(time.time() + 60)
    msg = await interaction.send(f"Go grab a coffee, this may take a while :D... ETA: <t:{ETA}:R>")
    generator = Craiyon()
    endResult = generator.generate(prompt)
    images = endResult.images
    GenLog = print(f'GenLog: "{prompt}"')
    for i in images:
        image = BytesIO(base64.decodebytes(i.encode("utf-8")))
        return await msg.edit(content="Image Generated! Make sure to visit **https://www.craiyon.com/** if ur cool :>", file = nextcord.File(image, f"{prompt}.png"))

##playlist command

@bot.slash_command(name="connect", description="Connects the bot to the VC")
async def connect(interaction: nextcord.Interaction):
    channel = interaction.user.voice.channel
    await channel.connect()
    await interaction.send("Bot has joined the VC!")

@bot.slash_command(name="disconnect",description="disconnects the bot from the VC")
async def leave(interaction: nextcord.Interaction):
    channel = interaction.user.voice.channel
    await interaction.disconnect()


## Say commandimage.png

@bot.slash_command(name="say", description="the bot says whatever you put in!")
async def say(interaction: nextcord.Interaction, *, message):
    ## SEND ORIGINAL MSG
    await interaction.send(f"{message}")

##ROLL COMMAND
@bot.slash_command(name='roll', description="The bot rolls a dice between the numbers that you chose!")
async def roll(interaction: nextcord.Interaction, min='1', max='100'): 
    RollLog = print(f"RollLog: Min {min} - Max {max}")
    print(RollLog)
    await interaction.send(random.randint(int(min), int(max)))

##GUESS COMMAND
@bot.slash_command(name="guess", description="Bot gets a number between 1 and 100 and you have to guess it")
@commands.cooldown(1, 60, commands.BucketType.user)
async def guess(interaction: nextcord.Interaction):
    await interaction.send("I thought of a number between **1 and 100, You got 5 guesses good luck!**")
    guesses = 5
    num = random.randint(1, 100)
    GuessLog = print(f"GuessLog: {num}")
    while True:
        msg = await bot.wait_for('message',check=lambda m:m.author == interaction.author and m.channel == interaction.channel and m.content.isdigit())
        guesses-=1
        num_ = int(msg.content)
        if num!=num_:
            await interaction.send(f"Incorrect! The number that I chose is {'**higher**' if num_<num else '**lower**'} you have *{guesses} guesses left*")
        else:
            await interaction.send(f"Correct! You guessed the number in **{5 - guesses} guesses!**")
            break
        if guesses == 0:
            await interaction.send(f"Incorrect! The number that I chose was **{num}**, better luck next time")
            break
## GUESS ERROR
@guess.error
async def Guess_error(interaction: nextcord.Interaction, error: commands.errors.CommandOnCooldown):
    if isinstance(error, commands.errors.CommandOnCooldown):
        await Interaction.send(f"You can only use this command once every 60 socends, Try again in {error.retry_after:.2f}s")
        return

##SOCIALS COMMAND
@bot.slash_command(name="socials")
async def socials(interaction: nextcord.Interaction):
    Twitch = Button(label="Twitch", url="https://www.twitch.tv/0minutesval", style = nextcord.ButtonStyle.blurple)
    Youtube = Button(label="Youtube", url="https://www.youtube.com/channel/UC4IZby3-37G0sZO0ZSDmCKg",style = nextcord.ButtonStyle.red)
    FriendTwitch = Button(label="Friends Twitch", url="https://www.twitch.tv/tvkrano",style = nextcord.ButtonStyle.blurple)

    myview = View(timeout=60)
    myview.add_item(Twitch)
    myview.add_item(Youtube)
    myview.add_item(FriendTwitch)
    await interaction.send("Twitch And Youtube! Make sure to follow and give me a sub ;) + my friend's twitch!", view=myview)

##WELCOME 

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        message = f"Welcome {member.mention} to {guild.name}. Make sure you check you #rules , bot prefix is '.' hopefully you will enjoy it here!"
        await guild.system_channel.send(message)

#### ------------------------------------------------------------------------------!!!MODERATION!!!-------------------------------------------------- ###


##VERIFICATION CHAT
@bot.slash_command(name="verification", description="verifies you!")
async def verification(interaction: nextcord.Interaction):

    user = interaction.user
    role = 1043889426008383502
    has_role = nextcord.utils.find(lambda r: r.name == 'Verified', interaction.guild.roles)
    datetime_object = datetime.now()

    ##
    if has_role in user.roles:
        ##FAIL EMBED
        embed = Embed(color=0xdb1414, description=f"{user.mention} you are already verified!")
        embed.set_author(name="Failure!")
        await interaction.send(embed=embed)

    else:
        ##SUCCESS EMBED
        embed = Embed(color=0x19942a, description=f"{user.mention}, you've been successfully verified at {datetime_object}! We hope you enjoy!")
        embed.set_author(name="Success!")

        await interaction.send(embed=embed)
        time.sleep(1.5)
        await user.add_roles(user.guild.get_role(role))

        

class verify(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        self.value = None
    
    @nextcord.ui.button(label="Verify", style=nextcord.ButtonStyle.success)
    async def demo1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role = 1043889426008383502
        user = interaction.user
        has_role =  nextcord.utils.find(lambda r: r.name == 'Verified', interaction.guild.roles)

        if has_role in user.roles:
            ##FAIL EMBED
            embed = Embed(color=0xdb1414, description=f"{user.mention} you are already verified!")
            embed.set_author(name="Failure!")
            await interaction.send(embed=embed, ephemeral=True)
        else:
            await user.add_roles(user.guild.get_role(role))
            ##SUCCESS EMBED
            datetime_object = datetime.now()
            embed = Embed(color=0x19942a, description=f"{user.mention}, you've been successfully verified at {datetime_object}! We hope you enjoy!")
            embed.set_author(name="Success!")
            await interaction.response.send_message(embed=embed, ephemeral=True)

##VERIFY
@commands.guild_only()
@commands.has_permissions(manage_messages = True)
@bot.slash_command(name="verify", description="embed verification command")
async def Verify(interaction: nextcord.Interaction):
    embed = Embed(color=0x2F3136, description="""Make sure you read the server <#1043886583838933014>. For any help message the owner <@692430762896523406> \n
    For bot help do .help and make sure to have fun! Incase you get an error saying "Interaction failed" run the command ".verification" in <#1043916857117249536>
    To Verify Click the button below :arrow_down:\n""")
    embed.set_author(name="SquadBot Verify", url="https://cdn.discordapp.com/emojis/947101075981340713.webp?size=96&quality=lossless")
    embed.set_footer(text=f"• Made By 0minutes")
    await interaction.channel.send(embed=embed, view = verify())

##RULES
@commands.guild_only()
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
@bot.slash_command(name="rules", description="The bot displays the default rules")
async def rules(interaction: nextcord.Interaction):
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
    await interaction.channel.send(embed=embed)
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
@bot.slash_command(description="clears given amount of messages.")
async def clear(interaction: nextcord.Interaction, amount: int = SlashOption(description="The amount of messages you want to clear.")):
    await interaction.channel.purge(limit=amount)
    pe = nextcord.Embed(description=f"Sucessfully purged {amount} messages!", color=0x2F3136, timestamp=datetime.now())
    pe.set_author(name="CLEAR SUCCESSFULL!")
    pe.set_footer(text=f"Executed by {interaction.user}")
    await interaction.send(embed=pe, delete_after=3)

##TICKET 

#CLOSE TICKET BUTTON CLASS + FUNCTION

class CloseTicket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        self.value = None

        
    @nextcord.ui.button(label="Close Ticket", style=nextcord.ButtonStyle.red)
    async def CloseTicket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel = interaction.channel
        await interaction.send("Ticket is closed...", ephemeral=True)
        time.sleep(1.1)
        await channel.delete()

        

#CREATE TICKET BUTTON CLASS + FUNCTION
class CreateTicket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        self.value = None
        
    
    @nextcord.ui.button(label="Create Ticket", style=nextcord.ButtonStyle.success)
    async def CreateTicket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        ##MAIN FUNCTION WHICH CREATES CHANNEL + GIVES OUT THE PERMS

        user = interaction.user
        guild = user.guild
        default_role = user.guild.get_role(1043889426008383502)
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
            user: nextcord.PermissionOverwrite(view_channel = True)
        }
        category = get(guild.categories, name="Tickets")
        await interaction.send("Ticket is being created...", ephemeral=True)
    ## WHEN THE USER PRESSES 
        
        channel = await guild.create_text_channel(name=f"ticket-{random.randint(1000, 9999)}", category = category, overwrites=overwrites) ##Makes a ticket channel in the the Tickets category + assigns a name

    ## SENDS THE CLOSE TICKET EMBED WHEN IN THE NEWLY CREATED CHANNEL
        
        CloseEmbed = Embed(color=0x2F3136, description="""So we can give you the best service please make sure you:!\n
    • Explained your question/problem in as much detail
    • Provide us with screenshots of the problem or accident (if any)
    • Be friendly to our staff members as they'll do their best to help you.\n
    To Close the ticket Click the button below :arrow_down:\n""")
        CloseEmbed.set_author(name="SquadBot Close Ticket",)
        CloseEmbed.set_footer(text=f"• Made By 0minutes")
        await channel.send(embed=CloseEmbed, view=CloseTicket())
        

        


@bot.slash_command(name="createticket", description="Creates a ticket embed + button!")
@commands.has_permissions(administrator=True)
async def Createticket(interaction: nextcord.Interaction):
    embed = Embed(color=0x2F3136, description="""If you have the smallest question or problem please be sure to share them here! We'll do everything in our power to help answer/solve your problem!\n
    To Create the ticket Click the button below :arrow_down:\n""")
    embed.set_author(name="SquadBot Create Ticket",)
    embed.set_footer(text=f"• Made By 0minutes")
    await interaction.channel.send(embed=embed, view=CreateTicket())


##BAN COMMAND
@bot.slash_command(name="ban", description="Ban a memeber from the discord server")
@commands.guild_only()
@commands.has_permissions(ban_members = True)
@commands.bot_has_permissions(ban_members = True)
async def ban(interaction: nextcord.Interaction, member: Member, *, reason:str=None):
    if reason == None:
        reason = "No reason provided"

    await member.ban(delete_message_days=0, reason=reason)
    await interaction.send(f"**{member.name} is banned for {reason}**")

##KICK COMMAND
@bot.slash_command(name="kick", description=("Kick a member from the server"))
@commands.guild_only()
@commands.has_permissions(kick_members = True)
@commands.bot_has_permissions(kick_members = True)
async def kick(interaction: nextcord.Interaction, member : nextcord.Member, *, reason=None):
    if reason == None:
        reason = "No reason provided"
    
    await member.kick(reason=reason)
    await interaction.send(f"**{member.name} is kicked for {reason}**")

### !!!ERROR HANDLER!!! ###

##KICK ERROR
@kick.error
async def kick_error(interaction: nextcord.Interaction, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await interaction.semnd(f"you do not have the kick members premissions")
        return
    
    elif isinstance(error, commands.BotMissingPermissions):
        await interaction.send(f"I dont have premissions to do that!")
        return

#BAN ERROR
@ban.error
async def ban_error(interaction: nextcord.Interaction, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await interaction.send(f"you do not have the ban members premissions")
        return
    
    elif isinstance(error, commands.BotMissingPermissions):
        await interaction.send(f"I dont have premissions to do that!")
        return

bot.run(config["token"])