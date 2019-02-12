#!/usr/bin/env python

import os
import cgi
import sys
from wmflabs import db
import json

#Print header
print('Content-type: application/json\n')

# Fetch params
if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	try:
		user_name = qs['user_name'][0]
	except:
		print('{"error": "user_name"}')
		sys.exit(0)
	try:
		new_format = qs['format'][0] == 'new'
	except:
		new_format = False
	try:
		wiki = qs['wiki'][0]
	except:
		wiki = 'cswiki'
else:
	print('{"error": "user_name"}')
	sys.exit(0)

##### PROGRAM ####

conn = db.connect(wiki)
cur = conn.cursor()
with cur:
	sql = 'select rc_this_oldid, rc_id from recentchanges_userindex where rc_user_text="%s" and rc_patrolled=0;' % user_name
	cur.execute(sql)
	if new_format:
		result = dict(cur.fetchall())
	else:
		result = []
		result.extend(row[1] for row in cur.fetchall())
	print(json.dumps(result))
