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
		rev_first = qs['rev_first'][0]
		rev_second = qs['rev_second'][0]
	except:
		print '{"error": "no rev_id"}'
		sys.exit(0)
else:
	print '{"error": "no rev_id"}'
	sys.exit(0)

##### PROGRAM ####

conn = db.connect('cswiki')
cur = conn.cursor()
with cur:
	sql = 'select rc_id from recentchanges where rc_this_oldid >= ' + rev_first + ' and rc_this_oldid <= ' + rev_second + ' and rc_patrolled=0;'
	cur.execute(sql)
	result = []
	for row in cur.fetchall():
		result.append(row[0])
	print json.dumps(result)
