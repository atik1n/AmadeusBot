from discord.ext import commands
import kurisu.prefs, traceback


class Events:
	def __init__(self, bot):
		self.bot = bot

	async def on_message(self, message):
		# if message.channel.id != "446333540381229066":
			# return

		if message.content == 'Nullpo':
			await message.channel.send('Gah!')

	async def on_command_error(self, ctx, error):
		ignored = (commands.CommandNotFound, commands.UserInputError)

		if isinstance(error, ignored):
			return

		tmpEmbed = kurisu.prefs.Embeds.new('error')
		tb = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__, limit=5)
		tmpEmbed.add_field(name="Вызвал", value=ctx.message.author.mention)
		tmpEmbed.add_field(name="Сообщение", value=ctx.message.content)
		tmpEmbed.add_field(name="Traceback", value='%s%s' % (''.join(tb[:5]), ''.join(tb[-1])))
		await kurisu.prefs.Channels.get('log').send(embed=tmpEmbed)

		if isinstance(error, commands.BadArgument):
			await ctx.message.channel.send('Ошибка в аргументе')
			return
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.message.channel.send('Недостаточно аргументов')
			return
		else:
			await ctx.message.channel.send('Упс... Информация об ошибке в %s' % kurisu.prefs.Channels.log.mention)


def setup(bot):
	bot.add_cog(Events(bot))
