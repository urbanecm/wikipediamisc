#!/usr/bin/env python

import os
import cgi
import sys
from wmflabs import db

#Print header
print 'Content-type: application/json\n'

# Fetch params
if 'QUERY_STRING' in os.environ:
	QS = os.environ['QUERY_STRING']
	qs = cgi.parse_qs(QS)
	try:
		rev_page = qs['rev_page'][0]
	except:
		print 'no rev_page'
		sys.exit(0)
else:
	print 'no rev_page'
	sys.exit(0)

##### PROGRAM ####

conn = db.connect('cswiki')
cur = conn.cursor()
with cur:
	sql = 'select rc_id from revision join recentchanges on rc_this_oldid=rev_id where rev_page=' + rev_page + ' and rc_patrolled=0;'
	cur.execute(sql)
	data = cur.fetchall()

result = data[0][0]
print result
