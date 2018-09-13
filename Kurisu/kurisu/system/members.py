import kurisu.prefs, sqlite3, datetime


class Events:
	def __init__(self, bot):
		self.bot = bot

	async def on_member_join(self, member):
		if member.guild != kurisu.prefs.Servers.get('FGL'):
			return
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		cursor.execute('select * from alpaca where userID = %s limit 1' % member.id)
		a = cursor.fetchall()

		tmpEmbed = kurisu.prefs.Embeds.new('welcome')
		tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(member))
		tmpEmbed.add_field(name="Никнейм", value=member)
		tmpEmbed.add_field(name="ID", value=member.id)
		if len(a) != 0:
			t = datetime.datetime.fromtimestamp(a[0][2]) - datetime.timedelta(hours=3)
			if t > datetime.datetime.now():
				pt = kurisu.prefs.parse_time(t.timetuple())
				pt = '%s %s' % (pt[0], pt[1])
				tmpEmbed.add_field(name="Альпакамен", value="до %s" % pt)
				await member.add_roles(kurisu.prefs.Roles.get('alpaca'))
			else:
				tmpEmbed.add_field(name="Альпакамен", value="Роль снята")
				cursor.execute('delete from alpaca where userID = %s' % member.id)
				conn.commit()
		tmpEmbed.set_image(url="https://i.imgur.com/DcLOkLK.gif")
		await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)
		conn.close()

	async def on_member_remove(self, member):
		if member.guild != kurisu.prefs.Servers.get('FGL'):
			return
		if member not in kurisu.prefs.Servers.get('FGL').members:
			return
		tmpEmbed = kurisu.prefs.Embeds.new('goodbye')
		tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(member))
		tmpEmbed.add_field(name="Никнейм", value=member)
		tmpEmbed.add_field(name="ID", value=member.id)
		tmpEmbed.set_image(url="https://i.imgur.com/72Al5af.gif")
		await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)

	async def on_member_ban(self, guild, user):
		if guild != kurisu.prefs.Servers.get('FGL'):
			return
		tmpEmbed = kurisu.prefs.Embeds.new('goodbye')
		tmpEmbed.title = "Лабмем забанен"
		tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(user))
		tmpEmbed.add_field(name="Никнейм", value=user)
		tmpEmbed.add_field(name="ID", value=user.id)
		tmpEmbed.add_field(name="Причина", value=kurisu.prefs.ban_check(await kurisu.prefs.Servers.get('FGL').bans(), user)[0].reason)
		tmpEmbed.set_image(url="https://i.imgur.com/HC5ZgV0.gif")
		await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)

	async def on_member_unban(self, guild, user):
		if guild != kurisu.prefs.Servers.get('FGL'):
			return
		tmpEmbed = kurisu.prefs.Embeds.new('welcome')
		tmpEmbed.title = "Лабмем разбанен"
		tmpEmbed.set_thumbnail(url=kurisu.prefs.avatar_url(user))
		tmpEmbed.add_field(name="Никнейм", value=user)
		tmpEmbed.add_field(name="ID", value=user.id)
		tmpEmbed.set_image(url="https://i.imgur.com/wupSJAh.gif")
		await kurisu.prefs.Channels.get('lab').send(embed=tmpEmbed)


def setup(bot):
	bot.add_cog(Events(bot))
