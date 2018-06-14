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
		rev_page = qs['rev_page'][0]
	except:
		print '{"error": "no rev_page"}'
		sys.exit(0)
	try:
		if len(qs['revids']) > 0:
			field = "rc_this_oldid"
		else:
			field = "rc_id"
	except:
		field = "rc_id"
else:
	print '{"error": "no rev_page"}'
	sys.exit(0)

##### PROGRAM ####

conn = db.connect('cswiki')
cur = conn.cursor()
with cur:
	sql = 'select %s from revision join recentchanges on rc_this_oldid=rev_id where rev_page=%s and rc_patrolled=0;' % (field, str(rev_page))
	cur.execute(sql)
	result = []
	for row in cur.fetchall():
		result.append(row[0])
	print json.dumps(result)
