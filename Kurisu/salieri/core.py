from discord.ext import commands
import signal, asyncio, sys, requests
import kurisu.prefs


class Bot(commands.Bot):
	fubuki = lambda text, desc, color: {'embeds': [{'color': color, 'title': text, 'description': desc}]}

	def _shut(self):
		desc = '{u.mention} отключена.'.format(u=kurisu.prefs.discordClient.user)
		requests.post(kurisu.prefs.webhook, json=self.fubuki("Ядро Salieri отключено.", desc, '15158332'))
		self._do_cleanup()

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
