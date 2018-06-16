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
		rev_page = int(qs['rev_page'][0])
		rev_first = int(qs['rev_first'][0])
		rev_second = int(qs['rev_second'][0])
	except:
		print '{"error": "no rev_id"}'
		sys.exit(0)
	try:
		new_format = qs['format'][0] == 'new'
	except:
		new_format = False
else:
	print '{"error": "no rev_id"}'
	sys.exit(0)

##### PROGRAM ####

conn = db.connect('cswiki')
cur = conn.cursor()
with cur:
	sql = 'select rc_this_oldid, rc_id from revision join recentchanges on rc_this_oldid=rev_id'
	sql += ' where rev_page=' + str(rev_page) + ' and rc_this_oldid > ' + str(rev_first) + ' and rc_this_oldid <= ' + str(rev_second) + ' and rc_patrolled=0;'
	cur.execute(sql)
	if new_format:
		result = dict(cur.fetchall())
	else:
		result.extend(row[1] for row in cur.fetchall())
	print json.dumps(result)
