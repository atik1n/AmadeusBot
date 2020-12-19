from vk_api import VkApi
from vk_api.audio import VkAudio
import kurisu.check, kurisu.prefs
from discord.ext import commands
import urllib, asyncio, discord

class vkAudio(commands.Cog, name='VKA'):
	"""BETA: Команды связанные со связью Моэки и ВК"""

	def __init__(self, bot):
		self.bot = bot
		self.session = VkApi('+79817573548', 'Nik0212Gans0412')
		self.session.auth()

		self.a = VkAudio(self.session)

	@commands.command(name='vkAdd')
	async def add(self, ctx, *track: str):
		"""Добавить первый трек в поиске.

		Аргументы:
		-----------
		q: `str`
			Название нужного трека.
		"""

		await ctx.send('Сейчас...')

		tracks = self.a.search(q=str(track), count=10)
		tracks = [track for track in tracks]

		if tracks:
			await ctx.send('Нашла `%s - %s`' % (tracks[0]['artist'], tracks[0]['title']))
			await ctx.send('>play %s' % tracks[0]['url'][:tracks[0]['url'].index('?')])
		else:
			await ctx.send('Ничего не нашлось')

	@commands.command(name='vkSearch')
	async def search(self, ctx, *track: str):
		"""Поиск аудиозаписи.

		Аргументы:
		-----------
		q: `str`
			Название нужного трека.
		"""

		await ctx.send('Сейчас...')

		tracks = self.a.search(q=str(track), count=10)
		tracks = [track for track in tracks]

		if tracks:
			if len(tracks) == 1:
				emb = kurisu.prefs.Embeds.new('alert')
				emb.colour = discord.Colour.green()
				emb.add_field(name="Автор", value=tracks[0]['artist'])
				emb.add_field(name="Название", value=tracks[0]['title'])
				emb.set_footer(text="Трек добавлен.")
				await ctx.send(embed=emb)
				await ctx.send('>play %s' % tracks[0]['url'][:tracks[0]['url'].index('?')])

			else:
				emb = kurisu.prefs.Embeds.new('alert')
				emb.add_field(name="Найдено",
							  value='\n'.join(['%s: %s - %s' % (str(i), track['artist'], track['title']) for i, track in enumerate(tracks, 1)]))
				emb.set_footer(text="Ожидание ввода...")
				mess = await ctx.send(embed=emb)

				def check(m):
					if m.content.isdigit() and ctx.message.author == m.author:
						return 0 <= int(m.content) <= 10
					else:
						return False
				try:
					m = await self.bot.wait_for('message', check=check, timeout=10)
				except asyncio.TimeoutError:
					m = None

				if m is None or m.content == '0':
					emb.clear_fields()
					emb.colour = discord.Colour.red()
					emb.add_field(name="Добавление трека", value="Добавление трека отменено.")
					emb.set_footer(text="Время ожидания вышло.")
					await mess.edit(embed=emb)
					return
				else:
					n = int(m.content) - 1
					emb.clear_fields()
					emb.colour = discord.Colour.green()
					emb.add_field(name="Автор", value=tracks[n]['artist'])
					emb.add_field(name="Название", value=tracks[n]['title'])
					emb.set_footer(text="Трек добавлен.")
					await mess.edit(embed=emb)
					await ctx.send('>play %s' % tracks[n]['url'][:tracks[n]['url'].index('?')])

				if m:
					await m.delete()
		else:
			await ctx.send('Ничего не нашлось')


def setup(bot):
	bot.add_cog(vkAudio(bot))