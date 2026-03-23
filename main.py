import discord
import random
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

STAFF_ROLE_NAME = "Staff"
role_message_id = None


def is_staff(member):
    return any(role.name == STAFF_ROLE_NAME for role in member.roles)


# ---------------- READY ----------------
@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game(name="ÆSTHETICA BOTʚ💝ɞ")
    )
    print("ÆSTHETICA BOT IS ONLINE")


# ---------------- WELCOME + AUTO ROLE ----------------
@client.event
async def on_member_join(member):
    channel = member.guild.system_channel

    if channel:
        embed = discord.Embed(
            title="⋆｡‧˚ʚ💝ɞ˚‧｡⋆ Welcome to ÆSTHETICA ⋆｡‧˚ʚ💝ɞ˚‧｡⋆",
            description=f"💗 Hey {member.mention}! Welcome ✨",
            color=0xFFB6C1
        )
        await channel.send(embed=embed)

    role = discord.utils.get(member.guild.roles, name="✨ Aesthetic Vibes")
    if role:
        try:
            await member.add_roles(role)
        except:
            pass


# ---------------- COMMANDS ----------------
@client.event
async def on_message(message):
    global role_message_id

    if message.author.bot:
        return

    content = message.content.lower()

    # HELLO
    if content == "!hello":
        await message.channel.send("🌸 Hello cutie!! 💕")

    # ROLES PANEL
    elif content == "!roles":
        embed = discord.Embed(
            title="🎀 Choose Your Aesthetic 🎀",
            description="💗 Pink Fairycore\n💙 Blue Blossom\n🌙 Midnight Dream",
            color=0xFFB6C1
        )

        msg = await message.channel.send(embed=embed)

        for emoji in ["💗", "💙", "🌙"]:
            await msg.add_reaction(emoji)

        role_message_id = msg.id

    # FAKE NITRO
    elif content == "!nitro":
        await message.channel.send("🎉 OMG YOU WON FREE NITRO!!! 💎✨")
        await asyncio.sleep(2)
        await message.channel.send("😭 Just kidding bestie!! Stay safe 💝")

    # 8BALL
    elif content.startswith("!8ball"):
        responses = [
            "💗 Absolutely yes.",
            "🌸 The vibes say yes.",
            "🌙 Maybe in your dream era.",
            "💔 Not right now."
        ]
        await message.channel.send(random.choice(responses))

    # COIN FLIP
    elif content == "!coinflip":
        await message.channel.send(random.choice(["💗 Heads!", "💙 Tails!"]))

    # COMPLIMENT
    elif content == "!compliment":
        compliments = [
            "🌸 You radiate positivity.",
            "💝 Your vibe is unmatched.",
            "✨ You're glowing today.",
            "🎀 Soft but powerful."
        ]
        await message.channel.send(random.choice(compliments))

    # CREATE TICKET
    elif content == "!ticket":
        guild = message.guild
        category = discord.utils.get(guild.categories, name="🎀 Support Tickets")

        if not category:
            category = await guild.create_category("🎀 Support Tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(
            f"ticket-{message.author.name}",
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🎀 Your Aesthetic Ticket 🎀",
            description=f"Welcome {message.author.mention} 💗\nType `!close` to close.",
            color=0xFFB6C1
        )

        await channel.send(embed=embed)
        await message.channel.send("💝 Your ticket has been created!")

    # CLOSE TICKET
    elif content == "!close":
        if message.channel.name.startswith("ticket-"):
            await message.channel.send("🧸 Closing ticket... ✨")
            await message.channel.delete()


# ---------------- REACTION ROLES ----------------
@client.event
async def on_raw_reaction_add(payload):
    global role_message_id

    if client.user is None or payload.user_id == client.user.id:
        return

    if role_message_id is None:
        return

    if payload.message_id != role_message_id:
        return

    guild = client.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        return

    role_dict = {
        "💗": "💗 Pink Fairycore",
        "💙": "💙 Blue Blossom",
        "🌙": "🌙 Midnight Dream"
    }

    emoji = str(payload.emoji)

    if emoji in role_dict:
        role = discord.utils.get(guild.roles, name=role_dict[emoji])
        if role:
            try:
                await member.add_roles(role)
            except:
                pass


client.run(TOKEN)
