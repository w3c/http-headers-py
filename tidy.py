#!/usr/local/bin/python
"""
CGI interface to tidy

running at http://cgi.w3.org/cgi-bin/tidy since Apr 2000.

Share and Enjoy. Open Source license:
Copyright (c) 2001 W3C (MIT, INRIA, Keio)
http://www.w3.org/Consortium/Legal/copyright-software-19980720
$Id$
 branched from v 1.11 2002/08/02 13:40:38 dom

"""

import cgi
import sys
import os
import urlparse
import urllib

Page = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US">
<head><title>HTML tidy service</title>
<link rel="stylesheet" href="http://www.w3.org/StyleSheets/base" />
</head>
<body>

<p><a href="http://www.w3.org/"><img src="http://www.w3.org/Icons/w3c_home" alt="W3C"/></a> <a href="http://www.w3.org/XML/">XML</a></p>

<h1>Tidy your HTML</h1>
"""
Page2 = """
<form method="GET">
<p>Address of document to tidy: <input name="docAddr" value="%s"/></p>
<p><input type="checkbox" name="indent" /> indent</p>
<p><input type="submit" value="get tidy results"/></p>
</form>

<hr />
<h2>Stuff used to build this service</h2>
<ul>
<li><a href="http://www.w3.org/People/Raggett/tidy/">tidy</a></li>
<li><a href="http://www.python.org/">python</a>, apache, etc.</li>
</ul>
<address>
script $Revision$ of $Date$<br />
by <a href="http://www.w3.org/People/Connolly/">Dan Connolly</a><br />
but I didn't do the real work, i.e. writing tidy
</address>
</body>
</html>
"""



def serveRequest():
    fields = cgi.FieldStorage()

    if not fields.has_key('docAddr'):
        print "Content-Type: text/html"
	print
        print Page
	print Page2 % ("")
    else:
        addr = fields['docAddr'].value
	if "'" in addr:
		print "Status: 403"
		print "Content-Type: text/plain"
		print
		print "sorry, I can't handle addresses with ' in them"
	elif addr[:5] == 'file:' or len(urlparse.urlparse(addr)[0])<2:
		print "Status: 403"
		print "Content-Type: text/plain"
		print
		print "sorry, I decline to handle file: addresses"
	else:
		opts='-n -asxml -q'
                import http_auth
		url_opener = http_auth.ProxyAuthURLopener()
		try:
			doc = url_opener.open(addr)
		except IOError, (errno, strerror):
			url_opener.error = "I/O error: %s %s" % (errno,strerror)
			doc = None
		print "Content-Type: text/html"
		print
		if doc:
			if fields.has_key('indent'): opts=opts + ' -i'
			command='/usr/bin/tr "\r" " "|/usr/local/bin/tidy %s 2>/dev/null' % opts
			po = os.popen(command,"w")
			sys.stdout.flush()
			po.write(doc.read())
		else:
			print Page
			print "<p style='color:#FF0000'>An error (%s) occured trying to get <a href='%s'>%s</a></p>" % (url_opener.error,addr,addr)
			print Page2 % addr


if __name__ == '__main__':
    if os.environ.has_key('SCRIPT_NAME'):
        serveRequest()
