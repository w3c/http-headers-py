W3c Spell Checker 

Share and Enjoy. Open Source license:
Copyright (c) 2001-2005 W3C (MIT, ERCIM, Keio)
http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231

Creator: Dominique Hazaël-Massieux dom@w3.org
Package compiled by: Patrick Shirkey pshirkey@boosthardware.com 

Decription:

This tool allows you to check the spelling of a web page. 
It currently only supports English and French.

Depends:

aspell
python
lynx

Install instructions:

Copy the spellchecker and http_auth scripts to your apache cgi-bin folder.

Usually this is located in:

/var/www/cgi-bin

chmod a+rx spellchecker http_auth.py

Edit the "languages" line to include the aspell dictionaries you want to use. On most distributions the dictionaries are located in

/usr/lib/aspell 

Edit the forms "action" link in the spellchecker script to direct it to the scripts location on your local server.

/cgi-bin/spellchecker

Notes:

Since http_auth.py is imported from the CGI script, it needs to be
in the path in which python will be looking for imported modules; you
have thus several options:
* put it in the same directory as the CGI script itself
* put it in one of the default python modules directories (e.g. in
Debian /usr/lib/python2.3/site-packages)
* edit the CGI script to add manually the directory in which python
should be looking for, with a line à la:
sys.path.insert(0, "/path/to/my/directory")

Note that you'll need this only if you indeed intend to use it on
HTTP-protected resources; if not, you could remove the module for good
by replacing the following 2 lines:

import http_auth
url_opener = http_auth.ProxyAuthURLopener()

by

import urllib
url_opener = urllib.FancyURLopener


