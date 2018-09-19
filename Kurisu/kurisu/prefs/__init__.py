import discord, copy, os, datetime, inspect
discordToken = "<token>"
webhook = '<url>'


def parse_time(dt):
	months = ['янв.', 'фев.', 'мар.', 'апр.', 'мая', 'июня', 'июля', 'авг.', 'сен.', 'окт.', 'ноя.', 'дек.']

	return ['%s %s %s' % (dt[2], months[dt[1]-1], dt[0]),  '%s:%s:%s' % (str(dt[3]).zfill(2), str(dt[4]).zfill(2), str(dt[5]).zfill(2))]


def ban_check(bans, user):
	return [x for x in bans if x.user.id == user.id]


def parse_delta(dt):
	s, d = dt.seconds, dt.days
	if d == 1:
		ds = "день"
	else:
		ds = "дней"
	h, s = s//3600, s % 3600
	m, s = s//60, s % 60

	return '%s %s, %s:%s:%s' % (tuple([str(d), ds, str(h).zfill(2), str(m).zfill(2), str(s).zfill(2)]))


def avatar_url(member):
	return 'https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.{1}'.format(member, 'gif' if member.is_avatar_animated() else 'png')


def info():
	info = []
	info.append(str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2)))
	info.extend(map(str, os.popen('free -t -m').readlines()[-1].split()[1:]))
	info.append(os.popen('vcgencmd measure_temp').readline())
	info[4] = info[4][info[4].index('=') + 1:info[4].rindex("'")]
	info.append(parse_delta(datetime.datetime.now()-startup))

	return info


discordClient = None
startup = None


class Objects:
	@classmethod
	def get(cls, name):
		try:
			return getattr(cls, name)
		except AttributeError:
			return None


class Servers(Objects):
	startup = [['FGL', 380104197267521537]]


class Embeds:
	error = discord.Embed(colour=discord.Colour.red())
	alert = discord.Embed(colour=discord.Colour.gold())
	normal = discord.Embed(colour=discord.Colour.dark_red())

	welcome = discord.Embed(colour=discord.Colour.green())
	welcome.title = "Новый Лабмем"

	goodbye = discord.Embed(colour=discord.Colour.red())
	goodbye.title = "Лабмем вышел"

	nyaa = discord.Embed(colour=discord.Colour.dark_red())
	dsgt = discord.Embed(colour=discord.Colour.dark_red())

	SG0 = discord.Embed(colour=discord.Colour.dark_red())

	def new(name):
		try:
			return copy.deepcopy(getattr(Embeds, name))
		except:
			return False

	def all():
		attributes = inspect.getmembers(Embeds, lambda a: not(inspect.isroutine(a)))
		return [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]


class Channels(Objects):
	startup = [['news', 'FGL', 430365781721743362],
				['lab', 'FGL', 380104197837815811],
				['log', 'FGL', 474683293304881175],
				['shower', 'FGL', 446333540381229066],
				['dev', 'FGL', 475059718562250752]]


class Roles(Objects):
	startup = [['alpaca', 'FGL', 474224730245955584],
				['sub', 'FGL', 492018941246570508]]


def init():
	for s in Servers.startup:
		setattr(Servers, s[0], discordClient.get_guild(s[1]))

	for c in Channels.startup:
		setattr(Channels, c[0], getattr(Servers, c[1]).get_channel(c[2]))

	for r in Roles.startup:
		setattr(Roles, r[0], [x for x in getattr(Servers, r[1]).roles if x.id == r[2]][0])

	for e in Embeds.all():
		e[1].set_author(name="Salieri Systems", icon_url="https://pp.userapi.com/c831209/v831209232/15d24c/tA_XzT7cXYA.jpg")

	Embeds.error.title = "Я ОШИБКА!!"

	Embeds.nyaa.set_thumbnail(url='https://sun9-6.userapi.com/c840635/v840635891/7bad7/o7JkD2yf8lg.jpg')
	Embeds.nyaa.title = 'Новые раздачи'

	Embeds.dsgt.set_thumbnail(url='https://pp.userapi.com/c846520/v846520774/54eed/7GAYm3VeAkk.jpg')
	# Embeds.dsgt.add_field(name='Disgusting Otaku', value = 'В 19:00 начинается трансляция нового эпизода на [dsgstng.com](https://dsgstng.com).\nНе пропустите! <:LeskisMirk:443050078047830018>')
	Embeds.dsgt.add_field(name="Disgusting Otaku", value="Телевизор сломался. Марш в вк в 19:00, лабмемы [vk.com/dsgtng](https://vk.com/dsgtng)\nКРЯЪ <:LeskisMirk:443050078047830018>")

	Embeds.SG0.set_thumbnail(url='https://sun9-6.userapi.com/c840635/v840635891/7bad7/o7JkD2yf8lg.jpg')
