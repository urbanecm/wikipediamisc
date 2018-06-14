#!/usr/bin/env python

import os
import cgi
import sys
from wmflabs import db
import json

#Print header
print 'Content-type: application/json\n'

# Fetch params
if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	try:
		user_name = qs['user_name'][0]
	except:
		print '{"error": "user_name"}'
		sys.exit(0)
else:
	print '{"error": "user_name"}'
	sys.exit(0)

##### PROGRAM ####

conn = db.connect('cswiki')
cur = conn.cursor()
with cur:
	sql = 'select rc_id from recentchanges where rc_user_text="%s"' % user_name
	cur.execute(sql)
	result = []
	for row in cur.fetchall():
		result.append(row[0])
	print json.dumps(result)
