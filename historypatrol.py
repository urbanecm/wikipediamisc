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
		rev_page = qs['rev_page'][0]
	except:
		print('{"error": "no rev_page"}')
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
	print('{"error": "no rev_page"}')
	sys.exit(0)

##### PROGRAM ####

conn = db.connect(wiki)
cur = conn.cursor()
with cur:
	sql = 'select rc_this_oldid, rc_id from revision join recentchanges on rc_this_oldid=rev_id where rev_page=%s and rc_patrolled=0;' % str(rev_page)
	cur.execute(sql)
	if new_format:
		result = dict(cur.fetchall())
	else:
		result = []
		result.extend(row[1] for row in cur.fetchall())
	print(json.dumps(result))
