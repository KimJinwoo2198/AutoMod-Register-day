import discord
import time
import json

token = 'token'

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_connect():
    with open('./setting.json', 'r') as d:
        data = json.load(d)
        setting = data['days']
        setting = int(setting)

@client.event
async def on_member_join(member):
    created = time.time - member.created_at.timestamp()
    created = int(created) / 86400
    created = round(created)

    if created < setting:
        embed = discord.Embed(title='Not enough days to create an account.', description=f'You have been kicked from **{member.guild}** because your account creation date is less than **{setting}** day.')
        await member.send(embed=embed)
        await member.kick(reason='Not enough days to create an account.')

@client.event
async def on_message(message):
    if message.content == '.!cmd':
        if message.author.guild_permissions.manage_messages:
            await message.channel.send('**.!edit**: Modify the date of creation.\n**.!settingv**: Shows the date of creation of the currently set criteria.')
    if message.content.startswith('.!edit'):
        if message.author.guild_permissions.manage_messages:
            m = message.content.split(" ")
            try:
                edit_amount = m[1]
            except:
                embed = discord.Embed(title='.!edit <number>')
                await message.channel.send(embed=embed)
                return

            if not edit_amount.isdecimal():
                embed = discord.Embed(title='.!edit <number>')
                await message.channel.send(embed=embed)
                return
            elif edit_amount.isdecimal():
                with open('./setting.json', 'r') as d:
                    data = json.load(d)
                data['days'] = edit_amount
                with open('./setting.json', 'w', encoding='utf-8') as m:
                    json.dump(data, m, indent="\t")
                d = data['days']
                await message.channel.send(f'It has been revised to `d`')

    if message.content == '!settingv':
        if message.author.guild_permissions.manage_messages:
            with open('./setting.json', 'r') as d:
                data = json.load(d)
            d1 = data['days']
            embed = discord.Embed(description="")
            embed.set_author(name=f'The currently set value is `{d1}`')
            await message.channel.send(embed=embed)

client.run(token)