from discord.ext import commands
import signal, asyncio, sys, requests
import kurisu.prefs


class NoPerms(commands.CheckFailure):
	pass


class Bot(commands.Bot):
	fubuki = lambda self, text, desc, color: {'embeds': [{'color': color, 'title': text, 'description': desc}]}

	def _shut(self):
		desc = '{u.mention} отключена.'.format(u=kurisu.prefs.discordClient.user)
		requests.post(kurisu.prefs.webhook, json=self.fubuki("Ядро Salieri отключено.", desc, '15158332'))
		self._do_cleanup()

	@staticmethod
	def log(name, text):
		if len(name) > 8:
			name = name[:8]

		print('[%s] | %s' % (name.ljust(8), text))

	def init_core(self, startup):
		for extension in startup[0]:
			try:
				self.load_extension(extension)
			except Exception as e:
				exc = '{}: {}'.format(type(e).__name__, e)
				print('Failed to load system extension {}\n{}'.format(extension, exc))

		for extension in startup[1]:
			try:
				self.load_extension(extension)
			except Exception as e:
				exc = '{}: {}'.format(type(e).__name__, e)
				print('Failed to load extension {}\n{}'.format(extension, exc))

	async def clear_webhook(self, channel):
		async for m in channel.history(limit=10):
			if (m.author.name == 'Fubuki-chan') and m.author.bot:
				await m.delete()

	def run(self, *args, **kwargs):
		is_windows = sys.platform == 'win32'
		loop = self.loop
		if not is_windows:
			loop.add_signal_handler(signal.SIGINT, self._shut)
			loop.add_signal_handler(signal.SIGTERM, self._shut)

		task = asyncio.ensure_future(self.start(*args, **kwargs), loop=loop)

		def stop_loop_on_finish(fut):
			loop.stop()

		task.add_done_callback(stop_loop_on_finish)

		try:
			loop.run_forever()
		except KeyboardInterrupt:
			print('Received signal to terminate bot and event loop.')
		finally:
			task.remove_done_callback(stop_loop_on_finish)
			if is_windows:
				self._shut()

			loop.close()
			if task.cancelled() or not task.done():
				return None
			return task.result()
