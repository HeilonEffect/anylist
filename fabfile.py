import os.path
import sqlite3
import sys

from fabric.api import env, execute, task, local

reload(sys)
sys.setdefaultencoding('utf-8')

@task
def backup(name='initial_data.json'):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	result = []
	groups = c.execute('SELECT * FROM apps_genre_group').fetchall()
	for group in groups:
		tmp = {}
		tmp['model'] = 'apps.genre_group'
		tmp['pk'] = group.id
		tmp['fields'] = {'name': group.name}
		result.append(tmp)

	for genre in c.fetchall('SELECT * FROM apps_genre'):
		tmp = {}
		tmp['model'] = 'apps.genre'
		tmp['pk'] = genre.id
		tmp['fields'] = {'name': genre.name, 'group': genre.group}
		result.append(tmp)

	for item in c.fetchall('SELECT * FROM apps_raiting'):
		tmp = {}
		tmp['model'] = 'apps.raiting'
