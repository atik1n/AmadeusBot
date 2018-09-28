import asyncio, datetime, sqlite3
from math import floor
import kurisu.prefs


async def alpacaLoop():
	ibn = kurisu.prefs.Channels.get('dev')
	alpacaRole = kurisu.prefs.Roles.get('alpaca')
	fgl = kurisu.prefs.Servers.get('FGL')
	dealp = [False, 0]
	while True:
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		if dealp[0]:
			cursor.execute('delete from alpaca where userID = %s' % dealp[1])
			u = fgl.get_member(int(dealp[1]))
			try:
				await u.remove_roles(alpacaRole)
				await ibn.send("%s больше не Альпакамен." % u.mention)
			except:
				await ibn.send("Пользователь с ID %s покинул сервер до снятия роли." % dealp[1])
			dealp = [False, '']
			conn.commit()

		cursor.execute('select * from alpaca order by date asc limit 1')
		a = cursor.fetchall()
		if len(a) != 0:
			t = datetime.datetime.fromtimestamp(a[0][2]) - datetime.timedelta(hours=3)
			r = floor((t - datetime.datetime.now()).total_seconds())
			if r <= 60:
				dealp = [True, str(a[0][1])]
				dt = r
				print(r)
			else:
				dt = 60
		else:
			dt = 60
		conn.close()
		await asyncio.sleep(dt)
