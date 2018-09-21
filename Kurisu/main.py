import discord, datetime

import kurisu.nyaa, kurisu.tips, kurisu.override, kurisu.alpaca, kurisu.prefs
import salieri.tasks, salieri.core
import requests

startup_extensions = ["kurisu.cogs.steins", "kurisu.cogs.upa", "kurisu.cogs.fgl", "kurisu.cogs.main"]
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
		print('[Discord] | Logged in as: %s | %s' % (client.user.name, client.user.id))
		await client.change_presence(activity=discord.Game(name='тестовый клиент', type=3))
		salieri.tasks.loop = client.loop
		await salieri.tasks.new(kurisu.nyaa.fetch)
		await salieri.tasks.new(kurisu.alpaca.alpacaLoop)
		kurisu.prefs.startup = datetime.datetime.now()

	desc = '{u.mention} готова к работе.'.format(u=client.user)
	requests.post(kurisu.prefs.webhook, json=fubuki("Ядро Salieri запущено.", desc, '3066993'))
	ready = True

if __name__ == "__main__":
	for extension in startup_system:
		try:
			client.load_extension(extension)
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			print('Failed to load system extension {}\n{}'.format(extension, exc))

	for extension in startup_extensions:
		try:
			client.load_extension(extension)
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(kurisu.prefs.discordToken)
