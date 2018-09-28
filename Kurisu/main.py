import discord, datetime

import kurisu.nyaa, kurisu.tips, kurisu.override, kurisu.alpaca, kurisu.prefs
import salieri.tasks, salieri.core
import requests

startup_extensions = ["kurisu.cogs.steins", "kurisu.cogs.upa", "kurisu.cogs.fgl", "kurisu.cogs.main", "kurisu.cogs.rp"]
startup_system = ["kurisu.system.messages", "kurisu.system.members"]

client = salieri.core.Bot(command_prefix='!', description='Salieri Systems', formatter=kurisu.override.newHelpFormatter())

ready = False
taskList = {}
fubuki = lambda text, desc, color: {'embeds': [{'color': color, 'title': text, 'description': desc}]}


@client.event
async def on_ready():
	global ready
	if ready:
		await kurisu.prefs.Channels.get('dev').send("Переподключение...")
	else:
		print('[Discord] | Initializing tips')
		kurisu.tips.init()
		print('[Discord] | Initializing preferences')
		kurisu.prefs.discordClient = client
		kurisu.prefs.init()
		print('[Salieri] | Initializing core')
		client.init_core([startup_system, startup_extensions])
		print('[Salieri] | Clearing Fubuki')
		await client.clear_webhook(kurisu.prefs.Channels.get('dev'))
		print('[Discord] | Logged in as: %s | %s' % (client.user.name, client.user.id))
		await client.change_presence(activity=discord.Activity(application_id='444126412270600202',
																name='Steins;Gate 0',
															   	type=3))
		salieri.tasks.loop = client.loop
		await salieri.tasks.new(kurisu.alpaca.alpacaLoop)
		kurisu.prefs.startup = datetime.datetime.now()

	desc = '{u.mention} готова к работе.'.format(u=client.user)
	requests.post(kurisu.prefs.webhook, json=fubuki("Ядро Salieri запущено.", desc, '3066993'))
	ready = True

client.run(kurisu.prefs.discordToken)
