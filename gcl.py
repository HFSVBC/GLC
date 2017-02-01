#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
GCL -> Get Comments and Likes Tool

With this tool you can get likes and comments from a facebook post.
All data is saved under CSV format.
"""

__author__ = "Hugo Filipe Curado"
__copyright__ = """
	This file is part of AVT.

    AVT is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    AVT is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with AVT.  If not, see <http://www.gnu.org/licenses/>."""
__version__ = "1.0"
__maintainer__ = "Hugo Filipe Curado"
__email__ = "hfsvbc@hugocurado.info"

import urllib, json, codecs, codecs

# ----------------- CONFIGURATION VARIABLES ------------------
access_toke = ""
page_id     = ""
post_id     = ""
# ------------------------------------------------------------
# ----------------------- HELP SECTION -----------------------
def linkContructor(page_id, post_id, action):
	global access_toke
	url      = "https://graph.facebook.com/"
	url      = url+page_id+"_"+post_id+action+"access_token="+access_toke
	response = urllib.urlopen(url)
	data     = json.loads(response.read())

	return  data

def getLikes(page_id, post_id):
	likes          = linkContructor(page_id, post_id, "/likes?")['data'];
	data_to_export = {}
	for l in likes:
		data_to_export[l[u'id']] = {'name': l['name']}
	return data_to_export

def getComments(page_id, post_id):
	comments = linkContructor(page_id, post_id, "/comments?")['data'];
	data_to_export = {}
	for c in comments:
		ps_id = c[u'id'].split('_')
		pg_id = ps_id[0]
		ps_id = ps_id[1]
		likes = linkContructor(pg_id, ps_id, '?fields=likes,like_count&')[u'like_count']
		try:
			data_to_export[c[u'from'][u'id']]['data'].append( (c['message'], likes))
		except KeyError:
			data_to_export[c[u'from'][u'id']] = {'name': c[u'from']['name'], 'data': [ (c['message'], likes)]}
		
	return data_to_export

def writeLikes(data):
	with codecs.open('glc_likes.csv', mode='w', encoding="ISO-8859-1") as fp:
		fp.write('user id;name')
		for l in data:
			fp.write("\n"+l+";"+data[l]['name'])

def writeComments(data):
	with codecs.open('gls_comments.csv', mode='w', encoding="ISO-8859-1") as fp:
		fp.write('user id;name;comments;comment likes')
		for c in data:
			for com in data[c]['data']:
				fp.write("\n"+c+";"+data[c]['name']+";"+com[0]+";"+str(com[1]))
# ------------------------------------------------------------
# ----------------------- MAIN SECTION -----------------------

print "LIKES"
writeLikes( getLikes(page_id, post_id))
print "COMMENTS"
writeComments( getComments(page_id, post_id))
# ------------------------------------------------------------